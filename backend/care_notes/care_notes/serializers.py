"""
Serializers for Care Notes Documentation
"""

from rest_framework import serializers
from .models import CareNote

class CareNoteSerializer(serializers.ModelSerializer):
    """Serializes CareNote model with author information"""
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    
    class Meta:
        model = CareNote
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']
