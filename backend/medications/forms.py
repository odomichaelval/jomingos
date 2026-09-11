from django import forms
from .models import Medication


class MedicationForm(forms.ModelForm):
    administered_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        error_messages={'required': 'Please enter the date and time administered.'}
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ ADDED THIS — prepend "— Select —" placeholder to Route and Type dropdowns
        self.fields['route'].choices = [('', '— Select Route —')] + list(self.fields['route'].choices)
        self.fields['med_type'].choices = [('', '— Select Type —')] + list(self.fields['med_type'].choices)

        # ✅ ADDED THIS — enforce required fields with friendly error messages
        required_fields = {
            'drug_name': 'Please enter the drug name.',
            'dosage': 'Please enter the dosage.',
            'route': 'Please select a route.',
            'med_type': 'Please select a type.',
            'reason': 'Please enter a reason / indication.',
        }
        for field_name, message in required_fields.items():
            self.fields[field_name].required = True
            self.fields[field_name].error_messages['required'] = message

        # ✅ ADDED THIS — same red-border pattern you used in VitalSignsForm
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                existing = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = existing + ' is-invalid'