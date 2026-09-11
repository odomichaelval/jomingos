from django.urls import path
from . import views

urlpatterns = [
    path('<int:patient_pk>/add/', views.add_care_note, name='add_care_note'),
    path('<int:patient_pk>/', views.care_note_list, name='care_note_list'),
    path('<int:patient_pk>/voice-transcribe/', views.voice_transcribe_care_note, name='voice_transcribe_care_note'),
    path('<int:patient_pk>/summarize/', views.summarize_care_notes, name='summarize_care_notes'),
    path('<int:patient_pk>/delete/<int:note_pk>/', views.delete_care_note, name='delete_care_note'),

]