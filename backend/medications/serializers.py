"""
Serializers for Medication Tracking
"""

from rest_framework import serializers
from .models import Medication

class MedicationSerializer(serializers.ModelSerializer):
    """Serializes Medication model with staff information"""
    administered_by_name = serializers.CharField(source='administered_by.get_full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    
    class Meta:
        model = Medication
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
