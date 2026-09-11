from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Added these new imports for voice transcriptiondatabse draft ↓
import os
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage

from patients.models import Patient
from .models import VitalSigns, VoiceVitalDraft   # ← added VoiceVitalDraft here
from .forms import VitalSignsForm
from .ai_service import transcribe_audio, extract_vitals_from_transcript  # ← add this


@login_required
def add_vitals(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    form = VitalSignsForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        v = form.save(commit=False)
        v.patient = patient
        v.recorded_by = request.user
        v.save()
        messages.success(request, f'Vital signs recorded for {patient.get_full_name()}.')
        return redirect('patient_detail', pk=patient_pk)
    return render(request, 'vitals/vitals_form.html', {'form': form, 'patient': patient})


@login_required
def vitals_list(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    vitals = VitalSigns.objects.filter(patient=patient).select_related('recorded_by')
    return render(request, 'vitals/vitals_list.html', {'patient': patient, 'vitals': vitals})


# ---- NEW VIEWS — ADD BELOW ↓ ----

@login_required
@require_POST
def voice_transcribe(request, patient_pk):
    """
    Receives audio blob from browser,
    transcribes with Whisper,
    extracts vitals with GPT,
    returns JSON to pre-fill the form.
    """
    patient = get_object_or_404(Patient, pk=patient_pk)
    audio_file = request.FILES.get('audio')

    if not audio_file:
        return JsonResponse({'error': 'No audio file received'}, status=400)
    
    # ✅ ADD THESE CHECKS
    allowed_types = ['audio/webm', 'audio/wav', 'audio/mp4', 'audio/mpeg']
    if audio_file.content_type not in allowed_types:
        return JsonResponse({'error': 'Invalid file type'}, status=400)

    if audio_file.size > 10 * 1024 * 1024:  # 10MB limit
        return JsonResponse({'error': 'Audio file too large. Max 10MB.'}, status=400)

    # Save audio temporarily to disk
    saved_path = default_storage.save(f'voice_vitals/temp_{audio_file.name}', audio_file)
    full_path = default_storage.path(saved_path)

    try:
        # Step 1 — Transcribe audio → text
        transcript = transcribe_audio(full_path)

        # Step 2 — Extract vitals from text → dictionary
        extracted = extract_vitals_from_transcript(transcript)

        # Step 3 — Save as a draft in the database
        draft = VoiceVitalDraft.objects.create(
            patient=patient,
            recorded_by=request.user,
            transcript=transcript,
            **{k: v for k, v in extracted.items() if v is not None}
        )

        # Step 4 — Send results back to the browser
        return JsonResponse({
            'draft_id': draft.id,
            'transcript': transcript,
            'vitals': extracted,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    finally:
        # Always clean up the temp audio file
        if os.path.exists(full_path):
            os.remove(full_path)


@login_required
def confirm_voice_draft(request, patient_pk, draft_pk):
    """
    Staff reviews the AI-extracted vitals,
    edits if needed, then saves as a real VitalSigns record.
    """
    patient = get_object_or_404(Patient, pk=patient_pk)
    draft = get_object_or_404(VoiceVitalDraft, pk=draft_pk, patient=patient)

    # Pre-fill the standard form with the AI draft values
    initial_data = {
        'temperature': draft.temperature,
        'bp_systolic': draft.bp_systolic,
        'bp_diastolic': draft.bp_diastolic,
        'heart_rate': draft.heart_rate,
        'respiratory_rate': draft.respiratory_rate,
        'oxygen_saturation': draft.oxygen_saturation,
        'blood_glucose': draft.blood_glucose,
        'weight_kg': draft.weight_kg,
        'pain_score': draft.pain_score,
        'notes': draft.notes,
    }

    form = VitalSignsForm(request.POST or None, initial=initial_data)

    if request.method == 'POST' and form.is_valid():
        v = form.save(commit=False)
        v.patient = patient
        v.recorded_by = request.user
        v.save()
        draft.status = 'confirmed'
        draft.save()
        messages.success(request, f'Vital signs confirmed for {patient.get_full_name()}.')
        return redirect('patient_detail', pk=patient_pk)

    return render(request, 'vitals/confirm_voice_draft.html', {
        'form': form,
        'patient': patient,
        'draft': draft,
        'transcript': draft.transcript,
    })
