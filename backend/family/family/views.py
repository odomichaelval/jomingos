from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from patients.models import Patient
from care_notes.models import CareNote
from vitals.models import VitalSigns
from medications.models import Medication
from .models import FamilyMember


def family_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role != 'family':
            messages.error(request, 'This area is for family members only.')
            return redirect('dashboard')
        try:
            request.user.family_profile
        except FamilyMember.DoesNotExist:
            messages.error(request, 'No family profile found. Please contact the care home.')
            return redirect('login')
        if not request.user.family_profile.approved:
            return render(request, 'family/not_approved.html')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@family_required
def family_portal(request):
    family_member = request.user.family_profile
    patient = family_member.patient
    now = timezone.now()
    last_7d = now - timedelta(days=7)

    recent_notes = CareNote.objects.filter(
        patient=patient,
        category__in=[
            'emotional', 'social', 'activity', 'nutrition',
            'hydration', 'sleep', 'observation_60', 'observation_30',
            'general', 'handover'
        ]
    ).select_related('author').order_by('-created_at')[:10]

    latest_vitals = VitalSigns.objects.filter(patient=patient).order_by('-recorded_at').first()
    weekly_notes_count = CareNote.objects.filter(patient=patient, created_at__gte=last_7d).count()

    mood_notes = CareNote.objects.filter(
        patient=patient, created_at__gte=last_7d
    ).exclude(mood='').select_related('author').order_by('-created_at')[:5]

    meal_notes = CareNote.objects.filter(
        patient=patient,
        category__in=['nutrition', 'hydration'],
        created_at__gte=last_7d
    ).order_by('-created_at')[:5]

    context = {
        'patient':            patient,
        'family_member':      family_member,
        'recent_notes':       recent_notes,
        'latest_vitals':      latest_vitals,
        'weekly_notes_count': weekly_notes_count,
        'mood_notes':         mood_notes,
        'meal_notes':         meal_notes,
        'now':                now,
    }
    return render(request, 'family/portal.html', context)


@family_required
def family_timeline(request):
    family_member = request.user.family_profile
    patient = family_member.patient

    notes = CareNote.objects.filter(
        patient=patient,
        category__in=[
            'emotional', 'social', 'activity', 'nutrition',
            'hydration', 'sleep', 'general', 'handover',
            'observation_eod', 'family_contact'
        ]
    ).select_related('author').order_by('-created_at')[:30]

    context = {
        'patient':       patient,
        'family_member': family_member,
        'notes':         notes,
    }
    return render(request, 'family/timeline.html', context)