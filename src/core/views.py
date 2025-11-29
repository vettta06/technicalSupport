from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from core.models import Ticket
from .decorators import role_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView


@login_required
def dashboard(request):
    return render(request, "dashboard.html", {"user": request.user})


@role_required(["respondent"])
def submit_data(request):
    return render(request, "submit_data.html")


@role_required(["admin"])
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")


@role_required(["provider"])
def provider_dashboard(request):
    return render(request, "provider_dashboard.html")


class CustomLogoutView(LogoutView):
    http_method_names = ["get", "post", "head", "options"]


@role_required(["respondent", "provider"])
def ticket_create(request):
    """Создание заявки"""
    if request.method == "POST":
        subject = request.POST.get("subject")
        description = request.POST.get("description")
        category = request.POST.get("category", "other")

        ticket = Ticket.objects.create(
            subject=subject,
            description=description,
            user=request.user,
            support_line=1,
            category=category,
        )
        if category in ["api_issue", "system_performance"]:
            ticket.support_line = 2
            ticket.status = "escalated"
            ticket.save()

        return redirect("ticket_list")
    return render(request, "tickets/create.html")


@role_required(["support"])
def ticket_list(request):
    """Список заявок"""
    if request.user.support_level == 1:
        tickets = Ticket.objects.filter(support_line=1).order_by("-created_at")
    elif request.user.support_level == 2:
        tickets = Ticket.objects.filter(
            support_line=request.user.support_level
        ).order_by("-created_at")
    else:
        tickets = Ticket.objects.none()
    return render(request, "tickets/list.html", {"tickets": tickets})


@role_required(["support"])
def ticket_escalate(request, ticket_id):
    """Эскалация заявки"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user.support_level != 1:
        return HttpResponseForbidden("Только L1 может эскалировать")
    if request.method == "POST":
        new_level = int(request.POST.get("to_level", 2))
        if new_level in [2, 3]:
            ticket.support_line = new_level
            ticket.status = "escalated"
            ticket.save()
            return redirect("ticket_list")
    return render(request, "tickets/escalate.html", {"ticket": ticket})


@role_required(["support"])
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user.support_level == 1 and ticket.support_line != 1:
        return HttpResponseForbidden(
            "Вы можете просматривать только заявки L1.")
    elif (
        request.user.support_level in [2, 3]
        and ticket.support_line != request.user.support_level
    ):
        return HttpResponseForbidden(
            "Вы можете просматривать только заявки вашего уровня."
        )
    return render(request, "tickets/detail.html", {"ticket": ticket})


@role_required(["support"])
def ticket_resolve(request, ticket_id):
    if request.method != "POST":
        return redirect("ticket_detail", ticket_id)
    ticket = get_object_or_404(Ticket, id=ticket_id)
    user = request.user
    if user.support_level == 1 and ticket.support_line == 1 and ticket.status == "open":
        ticket.status = "resolved"
        ticket.save()
    elif (
        user.support_level == 2
        and ticket.support_line == 2
        and ticket.status == "escalated"
    ):
        ticket.status = "resolved"
        ticket.save()

    return redirect("ticket_detail", ticket_id)
