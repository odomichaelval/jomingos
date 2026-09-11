from django import forms
from .models import VitalSigns


class VitalSignsForm(forms.ModelForm):
    recorded_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = VitalSigns
        fields = ['temperature', 'bp_systolic', 'bp_diastolic', 'heart_rate',
                  'respiratory_rate', 'oxygen_saturation', 'blood_glucose',
                  'weight_kg', 'pain_score', 'recorded_at', 'notes']
        widgets = {
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '37.0', 'step': '0.1'}),
            'bp_systolic': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '120'}),
            'bp_diastolic': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '80'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '72'}),
            'respiratory_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '16'}),
            'oxygen_saturation': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '98', 'step': '0.1'}),
            'blood_glucose': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '5.5', 'step': '0.1'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '70.0', 'step': '0.1'}),
            'pain_score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0', 'min': 0, 'max': 10}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    # ✅ ADDED THIS — runs after validation, adds red border to invalid fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Loop through all fields
        for field_name, field in self.fields.items():
            # If this field has errors, add is-invalid to its CSS class
            if self.errors.get(field_name):
                existing = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = existing + ' is-invalid'


    # ✅ ADD THIS — validates each field on submission
    def clean_temperature(self):
        val = self.cleaned_data.get('temperature')
        if val is not None and not (25.0 <= val <= 45.0):
            raise forms.ValidationError('Invalid value. Must be between 25–45°C.')
        return val

    def clean_bp_systolic(self):
        val = self.cleaned_data.get('bp_systolic')
        if val is not None and not (50 <= val <= 300):
            raise forms.ValidationError('Invalid value. Must be between 50–300 mmHg.')
        return val

    def clean_bp_diastolic(self):
        val = self.cleaned_data.get('bp_diastolic')
        if val is not None and not (30 <= val <= 200):
            raise forms.ValidationError('Invalid value. Must be between 30–200 mmHg.')
        return val

    def clean_heart_rate(self):
        val = self.cleaned_data.get('heart_rate')
        if val is not None and not (20 <= val <= 300):
            raise forms.ValidationError('Invalid value. Must be between 20–300 bpm.')
        return val

    def clean_respiratory_rate(self):
        val = self.cleaned_data.get('respiratory_rate')
        if val is not None and not (5 <= val <= 60):
            raise forms.ValidationError('Invalid value. Must be between 5–60 breaths/min.')
        return val

    def clean_oxygen_saturation(self):
        val = self.cleaned_data.get('oxygen_saturation')
        if val is not None and not (50.0 <= val <= 100.0):
            raise forms.ValidationError('Invalid value. Must be between 50–100%.')
        return val

    def clean_blood_glucose(self):
        val = self.cleaned_data.get('blood_glucose')
        if val is not None and not (1.0 <= val <= 50.0):
            raise forms.ValidationError('Invalid value. Must be between 1–50 mmol/L.')
        return val

    def clean_weight_kg(self):
        val = self.cleaned_data.get('weight_kg')
        if val is not None and not (1.0 <= val <= 300.0):
            raise forms.ValidationError('Invalid value. Must be between 1–300 kg.')
        return val

    def clean_pain_score(self):
        val = self.cleaned_data.get('pain_score')
        if val is not None and not (0 <= val <= 10):
            raise forms.ValidationError('Invalid value. Must be between 0–10.')
        return val
