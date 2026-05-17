from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from patients.models import Patient
from .models import CareNote
from .forms import CareNoteForm


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
    return render(request, 'care_notes/care_note_list.html', {
        'patient': patient, 'notes': notes,
        'category': category, 'category_choices': CareNote.CATEGORY_CHOICES,
    })
