from django.urls import path
from . import views

urlpatterns = [
    path('<int:patient_pk>/add/', views.add_medication, name='add_medication'),
    path('<int:patient_pk>/', views.medication_list, name='medication_list'),
    # New voice routes
    path('<int:patient_pk>/voice-transcribe/', views.voice_transcribe_medication, name='voice_transcribe_medication'),
    path('<int:patient_pk>/confirm-draft/<int:draft_pk>/', views.confirm_voice_medication_draft, name='confirm_voice_medication_draft'),
]
