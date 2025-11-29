from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('respondent/', views.submit_data, name='respondent'),
    path('admin_data/', views.admin_dashboard, name='admin_data'),
    path('provider/', views.provider_dashboard, name='provider'),
    path('tickets/create/', views.ticket_create, name='ticket_create'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/<int:ticket_id>/escalate/', views.ticket_escalate, name='ticket_escalate'),
]
