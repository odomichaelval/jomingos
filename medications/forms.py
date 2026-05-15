from django import forms
from .models import Medication


class MedicationForm(forms.ModelForm):
    administered_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Medication
        fields = ['drug_name', 'dosage', 'route', 'med_type', 'administered_at',
                  'reason', 'witnessed_by', 'refused', 'notes']
        widgets = {
            'drug_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Paracetamol'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 500mg'}),
            'route': forms.Select(attrs={'class': 'form-select'}),
            'med_type': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reason / indication'}),
            'witnessed_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Witness name'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'refused': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
