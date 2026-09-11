from django.urls import path
from . import views

urlpatterns = [
    path('<int:patient_pk>/add/', views.add_vitals, name='add_vitals'),
    path('<int:patient_pk>/', views.vitals_list, name='vitals_list'),
    # New voice routes
    path('<int:patient_pk>/voice-transcribe/', views.voice_transcribe, name='voice_transcribe'),
    path('<int:patient_pk>/confirm-draft/<int:draft_pk>/', views.confirm_voice_draft, name='confirm_voice_draft'),
]
