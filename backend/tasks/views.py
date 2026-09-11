from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from patients.models import Patient
from .models import CareTask
import datetime


# ── TASK DEFINITIONS ──────────────────────────────────────────────────────────
# Each entry: (task_type, shift, priority, due_time)

MORNING_TASKS = [
    ('obs_60_07',               'morning', 'medium', '07:00'),
    ('morning_wash',            'morning', 'medium', '07:30'),
    ('oral_care',               'morning', 'medium', '07:45'),
    ('dressing_assistance',     'morning', 'medium', '08:00'),
    ('morning_meds',            'morning', 'high',   '08:00'),
    ('breakfast',               'morning', 'medium', '08:15'),
    ('record_food_intake',      'morning', 'low',    '08:45'),
    ('fluid_intake_record',     'morning', 'medium', '09:00'),
    ('obs_60_08',               'morning', 'medium', '08:00'),
    ('obs_60_09',               'morning', 'medium', '09:00'),
    ('pressure_care_am',        'morning', 'high',   '09:15'),
    ('skin_integrity_check',    'morning', 'high',   '09:30'),
    ('temperature_check',       'morning', 'high',   '09:45'),
    ('blood_pressure_check',    'morning', 'high',   '09:50'),
    ('pulse_check',             'morning', 'high',   '09:55'),
    ('oxygen_saturation_check', 'morning', 'high',   '10:00'),
    ('pain_assessment',         'morning', 'high',   '10:05'),
    ('obs_60_10',               'morning', 'medium', '10:00'),
    ('mobility_assistance',     'morning', 'medium', '10:30'),
    ('wellbeing_check',         'morning', 'medium', '10:45'),
    ('mood_observation',        'morning', 'medium', '11:00'),
    ('obs_60_11',               'morning', 'medium', '11:00'),
    ('hand_hygiene_check',      'morning', 'medium', '11:15'),
    ('call_bell_check',         'morning', 'medium', '11:30'),
    ('obs_60_12',               'morning', 'medium', '12:00'),
    ('lunch',                   'morning', 'medium', '12:15'),
    ('assist_feeding',          'morning', 'medium', '12:20'),
    ('monitor_swallowing',      'morning', 'medium', '12:25'),
    ('lunch_meds',              'morning', 'high',   '12:30'),
    ('controlled_drug_check',   'morning', 'high',   '12:45'),
]

AFTERNOON_TASKS = [
    ('obs_60_13',               'afternoon', 'medium', '13:00'),
    ('record_food_intake',      'afternoon', 'low',    '13:15'),
    ('fluid_intake_record',     'afternoon', 'medium', '13:30'),
    ('encourage_fluids',        'afternoon', 'medium', '13:45'),
    ('repositioning_pm',        'afternoon', 'high',   '14:00'),
    ('pressure_care_pm',        'afternoon', 'high',   '14:15'),
    ('pressure_area_check',     'afternoon', 'high',   '14:30'),
    ('apply_barrier_cream',     'afternoon', 'medium', '14:45'),
    ('obs_60_14',               'afternoon', 'medium', '14:00'),
    ('physiotherapy_exercises', 'afternoon', 'medium', '14:30'),
    ('walking_support',         'afternoon', 'medium', '14:45'),
    ('fall_risk_monitoring',    'afternoon', 'high',   '15:00'),
    ('obs_60_15',               'afternoon', 'medium', '15:00'),
    ('afternoon_tea',           'afternoon', 'medium', '15:15'),
    ('nutritional_supplement',  'afternoon', 'medium', '15:30'),
    ('cognitive_stimulation',   'afternoon', 'medium', '15:45'),
    ('engage_social_activity',  'afternoon', 'low',    '16:00'),
    ('obs_60_16',               'afternoon', 'medium', '16:00'),
    ('respiration_rate_check',  'afternoon', 'high',   '16:15'),
    ('infection_symptom_check', 'afternoon', 'high',   '16:30'),
    ('room_safety_check',       'afternoon', 'medium', '16:45'),
    ('obs_60_17',               'afternoon', 'medium', '17:00'),
    ('dinner',                  'afternoon', 'medium', '17:15'),
    ('assist_feeding',          'afternoon', 'medium', '17:20'),
    ('special_diet_check',      'afternoon', 'medium', '17:25'),
    ('evening_meds',            'afternoon', 'high',   '17:30'),
    ('obs_60_18',               'afternoon', 'medium', '18:00'),
    ('evening_wash',            'afternoon', 'medium', '18:15'),
    ('oral_care_pm',            'afternoon', 'medium', '18:30'),
    ('skin_integrity_check',    'afternoon', 'high',   '18:45'),
    ('handover_note',           'afternoon', 'medium', '18:50'),
]

NIGHT_TASKS = [
    ('obs_60_19',               'night', 'medium', '19:00'),
    ('night_meds',              'night', 'high',   '20:00'),
    ('bed_position_check',      'night', 'medium', '20:15'),
    ('bed_rails_check',         'night', 'high',   '20:30'),
    ('comfort_check',           'night', 'medium', '20:45'),
    ('obs_60_20',               'night', 'medium', '20:00'),
    ('obs_60_21',               'night', 'medium', '21:00'),
    ('sleep_check',             'night', 'medium', '21:30'),
    ('obs_60_22',               'night', 'medium', '22:00'),
    ('night_round_check',       'night', 'medium', '22:30'),
    ('obs_60_23',               'night', 'medium', '23:00'),
    ('restlessness_monitoring', 'night', 'medium', '23:30'),
    ('obs_60_00',               'night', 'medium', '00:00'),
    ('repositioning_night',     'night', 'high',   '00:30'),
    ('pressure_ulcer_monitoring','night', 'high',   '01:00'),
    ('obs_60_01',               'night', 'medium', '01:00'),
    ('obs_60_02',               'night', 'medium', '02:00'),
    ('sleep_pattern_record',    'night', 'low',    '02:30'),
    ('obs_60_03',               'night', 'medium', '03:00'),
    ('obs_60_04',               'night', 'medium', '04:00'),
    ('obs_60_05',               'night', 'medium', '05:00'),
    ('obs_60_06',               'night', 'medium', '06:00'),
    ('temperature_check',       'night', 'high',   '06:15'),
    ('blood_pressure_check',    'night', 'high',   '06:20'),
    ('oxygen_saturation_check', 'night', 'high',   '06:25'),
    ('fire_exit_check',         'night', 'medium', '06:30'),
    ('emergency_equipment_check','night','medium',  '06:35'),
    ('lighting_check',          'night', 'low',    '06:40'),
]


def generate_daily_tasks(patient, date):
    all_tasks = MORNING_TASKS + AFTERNOON_TASKS + NIGHT_TASKS
    for task_type, shift, priority, due_time in all_tasks:
        CareTask.objects.get_or_create(
            patient=patient,
            task_type=task_type,
            due_date=date,
            defaults={
                'shift':    shift,
                'priority': priority,
                'due_time': due_time,
            }
        )


@login_required
def patient_checklist(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    date_str = request.GET.get('date', '')
    try:
        selected_date = datetime.date.fromisoformat(date_str)
    except ValueError:
        selected_date = timezone.now().date()

    generate_daily_tasks(patient, selected_date)

    tasks = CareTask.objects.filter(
        patient=patient, due_date=selected_date
    ).select_related('completed_by').order_by('due_time', 'task_type')

    morning   = tasks.filter(shift='morning')
    afternoon = tasks.filter(shift='afternoon')
    night     = tasks.filter(shift='night')

    total     = tasks.count()
    completed = tasks.filter(completed=True).count()
    percent   = int((completed / total) * 100) if total > 0 else 0

    high_total     = tasks.filter(priority='high').count()
    high_completed = tasks.filter(priority='high', completed=True).count()
    high_missed    = high_total - high_completed

    context = {
        'patient':       patient,
        'selected_date': selected_date,
        'morning':       morning,
        'afternoon':     afternoon,
        'night':         night,
        'total':         total,
        'completed':     completed,
        'percent':       percent,
        'high_total':    high_total,
        'high_completed':high_completed,
        'high_missed':   high_missed,
        'today':         timezone.now().date(),
    }
    return render(request, 'tasks/patient_checklist.html', context)


@login_required
@require_POST
def toggle_task(request, task_id):
    task = get_object_or_404(CareTask, pk=task_id)
    task.completed = not task.completed
    if task.completed:
        task.completed_by = request.user
        task.completed_at = timezone.now()
    else:
        task.completed_by = None
        task.completed_at = None
    task.save()
    return JsonResponse({
        'completed':    task.completed,
        'completed_by': task.completed_by.get_full_name() if task.completed_by else '',
        'completed_at': task.completed_at.strftime('%H:%M') if task.completed_at else '',
    })