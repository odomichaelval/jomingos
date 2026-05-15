from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from patients.models import Patient
from .models import VitalSigns
from .forms import VitalSignsForm


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
