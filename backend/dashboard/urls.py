from django.urls import path
from . import views, views_api

urlpatterns = [
    path('dashboard/admin/', views.admin_dashboard, name='role_dashboard_admin'),
    path('dashboard/doctor/', views.doctor_dashboard, name='role_dashboard_doctor'),
    path('dashboard/nurse/', views.nurse_dashboard, name='role_dashboard_nurse'),
    path('dashboard/care-assistant/', views.care_assistant_dashboard, name='role_dashboard_care_assistant'),
    path('', views.dashboard, name='dashboard'),
    path('handover/', views.shift_handover, name='shift_handover'),
    # Notification API endpoints
    path('api/notification/<int:notification_id>/read/', views_api.mark_notification_read, name='mark_notification_read'),
    path('api/preferences/dark-mode/', views_api.toggle_dark_mode, name='toggle_dark_mode'),
    # Shift API endpoints
    path('api/shifts/current/', views_api.UserShiftView.as_view(), name='get_current_shift'),
    path('api/shifts/set/', views_api.UserShiftView.as_view(), name='set_user_shift'),
]
