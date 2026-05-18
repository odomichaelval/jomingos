from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from patients.models import Patient
from .models import Medication
from .forms import MedicationForm


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
