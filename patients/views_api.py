"""
Patient Management API Views
Handles CRUD operations for patient records
"""

from rest_framework import viewsets, permissions
from .models import Patient
from .serializers import PatientSerializer

class IsNurseOrAdmin(permissions.BasePermission):
    """Custom permission - only nurses and admins can modify patients"""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ['admin', 'nurse']

class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint for patient management
    Provides list, create, retrieve, update, delete operations
    """
    queryset = Patient.objects.filter(is_active=True)
    serializer_class = PatientSerializer
    
    def get_permissions(self):
        """Different permissions for different actions"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsNurseOrAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        """Filter patients by search query"""
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            )
        return queryset
    
    def perform_create(self, serializer):
        """Save the current user as creator"""
        serializer.save(created_by=self.request.user)
