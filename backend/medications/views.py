from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from patients.models import Patient
from .models import Medication
from .forms import MedicationForm

# Added these new imports for voice transcriptiondatabse draft ↓

import os
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage

from .models import Medication, VoiceMedicationDraft
from .ai_service import transcribe_audio, extract_medication_from_transcript


@login_required
def add_medication(request, patient_pk):
    if request.user.role not in ('admin', 'nurse'):
        messages.error(request, 'Only nurses can record medications.')
        return redirect('patient_detail', pk=patient_pk)
    patient = get_object_or_404(Patient, pk=patient_pk)
    form = MedicationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        med = form.save(commit=False)
        med.patient = patient
        med.administered_by = request.user
        med.save()
        messages.success(request, f'Medication "{med.drug_name}" recorded for {patient.get_full_name()}.')
        return redirect('patient_detail', pk=patient_pk)
    return render(request, 'medications/medication_form.html', {'form': form, 'patient': patient})


@login_required
def medication_list(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    medications = Medication.objects.filter(patient=patient).select_related('administered_by')
    return render(request, 'medications/medication_list.html', {'patient': patient, 'medications': medications})



# ---- NEW VIEWS — ADDED BELOW ↓ ----




@login_required
@require_POST
def voice_transcribe_medication(request, patient_pk):
    """
    Receives audio blob from browser,
    transcribes with Whisper,
    extracts medication details with GPT,
    returns JSON to pre-fill the form.
    """
    patient = get_object_or_404(Patient, pk=patient_pk)
    audio_file = request.FILES.get('audio')

    if not audio_file:
        return JsonResponse({'error': 'No audio file received'}, status=400)

    allowed_types = ['audio/webm', 'audio/wav', 'audio/mp4', 'audio/mpeg']
    if audio_file.content_type not in allowed_types:
        return JsonResponse({'error': 'Invalid file type'}, status=400)

    if audio_file.size > 10 * 1024 * 1024:  # 10MB limit
        return JsonResponse({'error': 'Audio file too large. Max 10MB.'}, status=400)

    saved_path = default_storage.save(f'voice_medications/temp_{audio_file.name}', audio_file)
    full_path = default_storage.path(saved_path)

    try:
        # Step 1 — Transcribe audio → text
        transcript = transcribe_audio(full_path)

        # Step 2 — Extract medication details from text → dictionary
        extracted = extract_medication_from_transcript(transcript)

        # Step 3 — Save as a draft in the database
        draft = VoiceMedicationDraft.objects.create(
            patient=patient,
            recorded_by=request.user,
            transcript=transcript,
            **{k: v for k, v in extracted.items() if v is not None}
        )

        # Step 4 — Send results back to the browser
        return JsonResponse({
            'draft_id': draft.id,
            'transcript': transcript,
            'medication': extracted,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    finally:
        if os.path.exists(full_path):
            os.remove(full_path)


@login_required
def confirm_voice_medication_draft(request, patient_pk, draft_pk):
    """
    Staff reviews the AI-extracted medication details,
    edits if needed, then saves as a real Medication record.
    """
    patient = get_object_or_404(Patient, pk=patient_pk)
    draft = get_object_or_404(VoiceMedicationDraft, pk=draft_pk, patient=patient)

    initial_data = {
        'drug_name': draft.drug_name,
        'dosage': draft.dosage,
        'route': draft.route,        # Django matches this against ROUTE_CHOICES automatically
        'med_type': draft.med_type,  # same for MED_TYPE_CHOICES
        'reason': draft.reason,
        'notes': draft.notes,
    }

    form = MedicationForm(request.POST or None, initial=initial_data)

    if request.method == 'POST' and form.is_valid():
        med = form.save(commit=False)
        med.patient = patient
        med.administered_by = request.user
        med.save()
        draft.status = 'confirmed'
        draft.save()
        messages.success(request, f'Medication "{med.drug_name}" confirmed for {patient.get_full_name()}.')
        return redirect('patient_detail', pk=patient_pk)

    return render(request, 'medications/confirm_voice_draft.html', {
        'form': form,
        'patient': patient,
        'draft': draft,
        'transcript': draft.transcript,
    })