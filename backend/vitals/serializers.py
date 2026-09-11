"""
Serializers for Vital Signs Tracking
"""

from rest_framework import serializers
from .models import VitalSigns

class VitalSignsSerializer(serializers.ModelSerializer):
    """Serializes VitalSigns model with recorder information"""
    recorded_by_name = serializers.CharField(source='recorded_by.get_full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    
    class Meta:
        model = VitalSigns
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'recorded_at']
