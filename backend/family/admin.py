from django.contrib import admin
from .models import FamilyMember

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'patient', 'relation', 'approved']
    list_filter  = ['approved', 'relation']
    search_fields = ['user__first_name', 'user__last_name', 'patient__first_name']