from django.urls import path
from . import views

urlpatterns = [
    path('<int:patient_pk>/add/', views.add_care_note, name='add_care_note'),
    path('<int:patient_pk>/', views.care_note_list, name='care_note_list'),
]
