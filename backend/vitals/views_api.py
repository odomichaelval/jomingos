"""
Vital Signs API Views
Handles patient vital signs recording
"""

from rest_framework import viewsets, permissions
from .models import VitalSigns
from .serializers import VitalSignsSerializer

class VitalSignsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for vital signs
    All authenticated users can record and view vitals
    """
    queryset = VitalSigns.objects.all()
    serializer_class = VitalSignsSerializer
    
    def get_queryset(self):
        """Filter vitals by patient"""
        queryset = super().get_queryset()
        patient_id = self.request.query_params.get('patient')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset
    
    def perform_create(self, serializer):
        """Save the current user as recorder"""
        serializer.save(recorded_by=self.request.user)