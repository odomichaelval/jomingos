from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/admin/', views.admin_dashboard, name='role_dashboard_admin'),
    path('dashboard/doctor/', views.doctor_dashboard, name='role_dashboard_doctor'),
    path('dashboard/nurse/', views.nurse_dashboard, name='role_dashboard_nurse'),
    path('dashboard/care-assistant/', views.care_assistant_dashboard, name='role_dashboard_care_assistant'),
    path('', views.dashboard, name='dashboard'),
    path('handover/', views.shift_handover, name='shift_handover'),
]
