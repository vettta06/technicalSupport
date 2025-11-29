from django.shortcuts import render
from .decorators import role_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})


@role_required(['respondent'])
def submit_data(request):
    return render(request, 'submit_data.html')


@role_required(['admin'])
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


@role_required(['provider'])
def provider_dashboard(request):
    return render(request, 'provider_dashboard.html')


class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post', 'head', 'options']