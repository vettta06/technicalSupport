from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("admin_data/", views.admin_dashboard, name="admin_data"),
    path("provider/", views.provider_dashboard, name="provider"),
    path("tickets/create/", views.ticket_create, name="ticket_create"),
    path("tickets/", views.ticket_list, name="ticket_list"),
    path(
        'tickets/<int:ticket_id>/',
        views.ticket_detail,
        name='ticket_detail'
    ),
    path(
        'tickets/<int:ticket_id>/escalate/',
        views.ticket_escalate,
        name='ticket_escalate'
    ),
    path(
        'tickets/<int:ticket_id>/resolve/',
        views.ticket_resolve,
        name='ticket_resolve'
    ),
    path('api/data/', views.api_data_submission, name='api_data_submission'),
    path("submit-data/", views.submit_data, name="submit_data"),
    path("upload-offline/", views.upload_offline, name="upload_offline"),
    path("notifications/", views.notifications, name='notifications'),
]
