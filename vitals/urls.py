from django.urls import path
from . import views

urlpatterns = [
    path('<int:patient_pk>/add/', views.add_vitals, name='add_vitals'),
    path('<int:patient_pk>/', views.vitals_list, name='vitals_list'),
]
