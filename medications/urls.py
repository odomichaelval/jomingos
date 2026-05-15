from django.urls import path
from . import views

urlpatterns = [
    path('<int:patient_pk>/add/', views.add_medication, name='add_medication'),
    path('<int:patient_pk>/', views.medication_list, name='medication_list'),
]
