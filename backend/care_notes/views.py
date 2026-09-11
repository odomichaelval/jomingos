from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from patients.models import Patient
from .models import CareNote
from .forms import CareNoteForm
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST


# Added these new imports for voice transcriptiondatabse draft ↓

import os
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage

from .models import CareNote, VoiceCareNoteDraft, CareNoteSummaryEvaluation
from .ai_service import (
    transcribe_audio,
    extract_care_note_from_transcript,
    summarize_care_notes_period,
    compute_summary_metrics,
    build_evidence_links,
)


from datetime import datetime
from django.utils import timezone as tz
from .ai_service import summarize_care_notes_period


@login_required
def add_care_note(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    form = CareNoteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        note = form.save(commit=False)
        note.patient = patient
        note.author = request.user
        note.save()
        messages.success(request, f'Care note recorded for {patient.get_full_name()}.')
        return redirect('patient_detail', pk=patient_pk)
    return render(request, 'care_notes/care_note_form.html', {'form': form, 'patient': patient})



@login_required
def care_note_list(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    notes = CareNote.objects.filter(patient=patient).select_related('author')
    category = request.GET.get('category', '')
    if category:
        notes = notes.filter(category=category)

    paginator = Paginator(notes, 10)  # 10 notes per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'care_notes/care_note_list.html', {
        'patient': patient, 'notes': page_obj,  # note: notes is now the page object
        'category': category, 'category_choices': CareNote.CATEGORY_CHOICES,
    })


@login_required
@require_POST
def voice_transcribe_care_note(request, patient_pk):
    """
    Receives audio blob from browser, transcribes with Whisper,
    structures it into a professional note with GPT, saves a draft,
    and returns the result so JS can pre-fill the notes textarea.
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

    saved_path = default_storage.save(f'voice_care_notes/temp_{audio_file.name}', audio_file)
    full_path = default_storage.path(saved_path)

    try:
        # Step 1 — Transcribe audio → text
        transcript = transcribe_audio(full_path)

        # Guard 1 — catch empty/near-silent audio before it reaches GPT.
        # Whisper can hallucinate plausible-sounding words from silence or
        # background noise, so a very short transcript is treated as "nothing said".
        if not transcript or len(transcript.split()) < 4:
            return JsonResponse({
                'error': 'No clear speech detected. Please try recording again, closer to the microphone.'
            }, status=400)

        # Step 2 — Structure transcript into a professional note
        structured_note = extract_care_note_from_transcript(transcript)

        # Guard 2 — GPT itself may determine the transcript had no real
        # care content (e.g. background chatter that still forms real words).
        if structured_note.strip() == "NO_CONTENT":
            return JsonResponse({
                'error': 'No clear care-related content detected in the recording. Please try again.'
            }, status=400)

        # Step 3 — Save as a draft for audit trail
        draft = VoiceCareNoteDraft.objects.create(
            patient=patient,
            recorded_by=request.user,
            transcript=transcript,
            structured_note=structured_note,
        )

        # Step 4 — Send result back to the browser
        return JsonResponse({
            'draft_id': draft.id,
            'transcript': transcript,
            'structured_note': structured_note,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    finally:
        if os.path.exists(full_path):
            os.remove(full_path)

  
  # Period and selected care note summary view


@login_required
@require_POST
def summarize_care_notes(request, patient_pk):
    """
    Reads a date range, pulls this patient's care notes within that range,
    generates an AI summary, evaluates it (ROUGE/BLEU/BERTScore) against
    the source notes, builds evidence links (which note backs which summary
    sentence), saves the full result, and returns it to the browser.
    """
    patient = get_object_or_404(Patient, pk=patient_pk)

    start_str = request.POST.get('start_date')
    end_str = request.POST.get('end_date')

    if not start_str or not end_str:
        return JsonResponse({'error': 'Please select a start and end date.'}, status=400)

    try:
        start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format.'}, status=400)

    if start_date > end_date:
        return JsonResponse({'error': 'Start date must be before end date.'}, status=400)

    start_dt = tz.make_aware(datetime.combine(start_date, datetime.min.time()))
    end_dt = tz.make_aware(datetime.combine(end_date, datetime.max.time()))

    notes = CareNote.objects.filter(
        patient=patient,
        created_at__gte=start_dt,
        created_at__lte=end_dt,
    ).select_related('author')

    if not notes.exists():
        return JsonResponse({
            'error': f'No care notes recorded for {patient.get_full_name()} in that period.'
        }, status=404)

    note_list = list(notes)

    # Step 1 — Generate the summary
    summary = summarize_care_notes_period(note_list)

    if summary.strip() == "NO_CONTENT":
        return JsonResponse({
            'error': 'Not enough recorded detail in this period to generate a meaningful summary.'
        }, status=404)

    # Step 2 — Evaluate the summary against the source notes
    source_notes_text = "\n".join(n.note_text for n in note_list)
    metrics = compute_summary_metrics(summary, source_notes_text)

    # Step 3 — Build evidence links (which note backs which summary sentence)
    evidence_links = build_evidence_links(summary, note_list)

    # Step 4 — Save the full evaluation record
    evaluation = CareNoteSummaryEvaluation.objects.create(
        patient=patient,
        generated_by=request.user,
        period_start=start_date,
        period_end=end_date,
        source_note_count=len(note_list),
        summary_text=summary,
        rouge1=metrics['rouge1'],
        rouge2=metrics['rouge2'],
        rougeL=metrics['rougeL'],
        bleu=metrics['bleu'],
        bertscore_precision=metrics['bertscore_precision'],
        bertscore_recall=metrics['bertscore_recall'],
        bertscore_f1=metrics['bertscore_f1'],
        evidence_links=evidence_links,
    )

    # Step 5 — Return everything to the browser
    return JsonResponse({
        'evaluation_id': evaluation.id,
        'summary': summary,
        'note_count': len(note_list),
        'start_date': start_str,
        'end_date': end_str,
        'metrics': metrics,
        'evidence_links': evidence_links,
    })

#to delete care note
@login_required
@require_POST
def delete_care_note(request, patient_pk, note_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    note = get_object_or_404(CareNote, pk=note_pk, patient=patient)
    note.delete()
    messages.success(request, 'Care note deleted.')
    return redirect('care_note_list', patient_pk=patient_pk)