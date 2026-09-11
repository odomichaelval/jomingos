from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    admission_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender', 'nhs_number',
            'blood_group', 'room_number', 'admission_date', 'care_level', 'primary_nurse',
            'allergies', 'medical_conditions', 'dietary_requirements', 'mobility_status',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation',
            'gp_name', 'gp_phone', 'photo',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ('date_of_birth', 'admission_date'):
                widget_class = field.widget.__class__.__name__
                if widget_class in ('TextInput', 'Select', 'NumberInput', 'EmailInput', 'URLInput'):
                    field.widget.attrs['class'] = 'form-control'
                elif widget_class == 'Textarea':
                    field.widget.attrs['class'] = 'form-control'
                    field.widget.attrs['rows'] = 3
                elif widget_class == 'FileInput':
                    field.widget.attrs['class'] = 'form-control'
        self.fields['nhs_number'].required = False
        self.fields['primary_nurse'].widget.attrs['class'] = 'form-select'
        self.fields['care_level'].widget.attrs['class'] = 'form-select'
        self.fields['gender'].widget.attrs['class'] = 'form-select'
        self.fields['blood_group'].widget.attrs['class'] = 'form-select'
