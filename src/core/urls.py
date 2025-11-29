from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('respondent/', views.submit_data, name='respondent'),
    path('admin_data/', views.admin_dashboard, name='admin_data'),
    path('provider/', views.provider_dashboard, name='provider'),
]
