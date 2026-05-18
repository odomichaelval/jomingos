"""
Medication API Views
Handles medication administration tracking
"""

from rest_framework import viewsets, permissions
from .models import Medication
from .serializers import MedicationSerializer

class IsNurseOrAdmin(permissions.BasePermission):
    """Only nurses and admins can record medications"""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ['admin', 'nurse']

class MedicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for medication records
    Nurses can create, all staff can view
    """
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAuthenticated(), IsNurseOrAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        """Filter medications by patient"""
        queryset = super().get_queryset()
        patient_id = self.request.query_params.get('patient')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset
    
    def perform_create(self, serializer):
        """Save the current user as administrator"""
        serializer.save(administered_by=self.request.user)
