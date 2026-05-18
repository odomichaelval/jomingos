"""
Serializers for Patient Management
Converts Patient model to JSON for API
"""

from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    """Serializes Patient model with calculated fields"""
    age = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def get_full_name(self, obj):
        """Returns patient's full name"""
        return f"{obj.first_name} {obj.last_name}"

    def get_age(self, obj):
        return obj.get_age()

    def get_created_by_name(self, obj):
        if not obj.created_by:
            return ""
        return obj.created_by.get_full_name() or obj.created_by.username
