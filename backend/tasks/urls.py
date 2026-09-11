from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/checklist/', views.patient_checklist, name='patient_checklist'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
]