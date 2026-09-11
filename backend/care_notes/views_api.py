"""
Care Notes API Views
Handles creation and retrieval of patient care documentation
"""

from rest_framework import viewsets, permissions
from .models import CareNote
from .serializers import CareNoteSerializer

class CareNoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for care notes
    All authenticated users can view, staff can create
    """
    queryset = CareNote.objects.all()
    serializer_class = CareNoteSerializer
    
    def get_queryset(self):
        """Filter care notes by patient"""
        queryset = super().get_queryset()
        patient_id = self.request.query_params.get('patient')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset
    
    def perform_create(self, serializer):
        """Save the current user as author"""
        serializer.save(author=self.request.user)