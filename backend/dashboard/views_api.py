"""
Dashboard API Views
Provides summary statistics and role-scoped dashboard payloads.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import timedelta, datetime, time
from accounts.models import User
from patients.models import Patient
from care_notes.models import CareNote
from medications.models import Medication
from vitals.models import VitalSigns
from .models import DashboardNotification, DashboardPreference, UserShift


ROLE_ROUTE_MAP = {
    "admin": "admin",
    "doctor": "doctor",
    "nurse": "nurse",
    "care-assistant": "care_assistant",
}


ROLE_DASHBOARD_COPY = {
    "admin": {
        "title": "Administrator Command Centre",
        "subtitle": "Operational visibility across residents, staffing, records, and risk.",
        "focus": ["Staff coverage", "Clinical governance", "Resident safety", "Audit readiness"],
    },
    "doctor": {
        "title": "Doctor Clinical Workspace",
        "subtitle": "Prioritise reviews, risk signals, medication history, and clinical observations.",
        "focus": ["High-risk reviews", "Medication oversight", "NEWS2 trends", "Clinical notes"],
    },
    "nurse": {
        "title": "Nurse Shift Dashboard",
        "subtitle": "Coordinate observations, medications, notes, and handover activity for the shift.",
        "focus": ["Medication rounds", "Vitals due", "Shift handover", "Resident notes"],
    },
    "care_assistant": {
        "title": "Care Assistant Daily Care Hub",
        "subtitle": "Stay close to personal care, wellbeing notes, routines, and resident support tasks.",
        "focus": ["Personal care", "Wellbeing checks", "Daily activities", "Escalations"],
    },
}

class DashboardStatsView(APIView):
    """
    API endpoint for dashboard statistics
    GET /api/dashboard/stats/
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Return summary statistics for the dashboard"""
        today = timezone.localdate()
        
        stats = {
            'total_patients': Patient.objects.filter(is_active=True).count(),
            'notes_today': CareNote.objects.filter(created_at__date=today).count(),
            'staff_count': User.objects.filter(is_active=True).count(),
            'medications_today': Medication.objects.filter(administered_at__date=today).count(),
        }
        return Response(stats)


class RoleDashboardView(APIView):
    """
    GET /api/dashboard/<role>/
    Returns dashboard data only when the authenticated user's role matches.
    This is the backend access-control gate used by the role-specific frontend pages.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, role):
        requested_role = ROLE_ROUTE_MAP.get(role)
        if requested_role is None:
            return Response({"detail": "Unknown dashboard role."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role != requested_role:
            return Response(
                {"detail": "You do not have permission to access this dashboard."},
                status=status.HTTP_403_FORBIDDEN,
            )

        today = timezone.localdate()
        last_24h = timezone.now() - timedelta(hours=24)
        high_risk_count = 0
        observations_due = 0

        for patient in Patient.objects.filter(is_active=True):
            latest_vitals = VitalSigns.objects.filter(patient=patient).order_by("-recorded_at").first()
            if not latest_vitals:
                observations_due += 1
                continue
            if latest_vitals.news2_level == "high":
                high_risk_count += 1
            if latest_vitals.recorded_at < last_24h:
                observations_due += 1

        recent_notes = CareNote.objects.select_related("patient", "author").order_by("-created_at")[:5]
        recent_medications = Medication.objects.select_related("patient", "administered_by").order_by("-administered_at")[:5]

        payload = {
            "user": {
                "username": request.user.username,
                "full_name": request.user.get_full_name(),
                "role": request.user.role,
                "role_display": request.user.get_role_display(),
            },
            "profile": ROLE_DASHBOARD_COPY[requested_role],
            "metrics": {
                "active_patients": Patient.objects.filter(is_active=True).count(),
                "notes_today": CareNote.objects.filter(created_at__date=today).count(),
                "medications_today": Medication.objects.filter(administered_at__date=today).count(),
                "staff_on_duty": User.objects.filter(is_active=True, is_on_duty=True).count(),
                "high_risk_patients": high_risk_count,
                "observations_due": observations_due,
            },
            "activity": [
                {
                    "kind": "Care note",
                    "title": f"{note.get_category_display()} note",
                    "detail": f"{note.patient} by {note.author.get_full_name() or note.author.username}",
                    "time": note.created_at,
                }
                for note in recent_notes
            ],
            "medication_activity": [
                {
                    "kind": "Medication",
                    "title": f"{med.drug_name} {med.dosage}",
                    "detail": f"{med.patient} by {med.administered_by.get_full_name() or med.administered_by.username}",
                    "time": med.administered_at,
                }
                for med in recent_medications
            ],
        }
        return Response(payload)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    notification = get_object_or_404(DashboardNotification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_dark_mode(request):
    """Toggle dark mode preference for user"""
    pref, created = DashboardPreference.objects.get_or_create(user=request.user)
    pref.dark_mode = not pref.dark_mode
    pref.save()
    return JsonResponse({'dark_mode': pref.dark_mode})


class UserShiftView(APIView):
    """
    API endpoint for user shift management
    GET /api/shifts/current/ - Get current user's active shift
    POST /api/shifts/set/ - Set or update user's shift
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current user's shift for today"""
        today = timezone.localdate()
        try:
            shift = UserShift.objects.get(user=request.user, shift_date=today, is_active=True)
            return Response({
                'user': request.user.username,
                'shift_type': shift.shift_type,
                'start_time': shift.start_time.strftime('%H:%M'),
                'end_time': shift.end_time.strftime('%H:%M'),
                'time_remaining_minutes': shift.time_remaining_minutes,
                'time_remaining_formatted': shift.time_remaining_formatted,
                'progress_percent': shift.shift_progress_percent,
                'notes': shift.notes,
            })
        except UserShift.DoesNotExist:
            # Return default shift if none exists
            now = timezone.now()
            hour = now.hour

            if 7 <= hour < 19:
                shift_type = 'day'
                start_time = '07:00'
                end_time = '19:00'
            else:
                shift_type = 'night'
                start_time = '19:00'
                end_time = '07:00'

            return Response({
                'user': request.user.username,
                'shift_type': shift_type,
                'start_time': start_time,
                'end_time': end_time,
                'time_remaining_minutes': 0,
                'time_remaining_formatted': '00:00',
                'progress_percent': 0,
                'notes': 'No shift scheduled',
            })

    def post(self, request):
        """Create or update user's shift"""
        shift_type = request.data.get('shift_type', 'day')
        start_time_str = request.data.get('start_time', '07:00')
        end_time_str = request.data.get('end_time', '19:00')
        notes = request.data.get('notes', '')

        try:
            # Parse time strings
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
        except ValueError:
            return Response(
                {'error': 'Invalid time format. Use HH:MM format.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        today = timezone.localdate()

        # Create or update shift
        shift, created = UserShift.objects.update_or_create(
            user=request.user,
            shift_date=today,
            defaults={
                'shift_type': shift_type,
                'start_time': start_time,
                'end_time': end_time,
                'notes': notes,
                'is_active': True,
            }
        )

        return Response({
            'success': True,
            'message': 'Shift scheduled successfully',
            'shift_type': shift.shift_type,
            'start_time': shift.start_time.strftime('%H:%M'),
            'end_time': shift.end_time.strftime('%H:%M'),
            'time_remaining_minutes': shift.time_remaining_minutes,
            'time_remaining_formatted': shift.time_remaining_formatted,
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
