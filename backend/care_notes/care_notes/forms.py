from django import forms
from .models import CareNote


class CareNoteForm(forms.ModelForm):

    class Meta:
        model = CareNote
        fields = [
            'category', 'priority', 'note_text',
            # Observation
            'obs_location', 'obs_status', 'obs_completed',
            # Personal care
            'wash_type', 'oral_care', 'continence', 'pressure_area',
            'repositioned', 'repositioned_position',
            # Nutrition
            'meal_time', 'appetite', 'fluid_intake', 'fluid_amount_ml', 'weight_kg',
            # Wellbeing
            'mood', 'sleep_quality', 'sleep_hours',
            # Mobility
            'mobility_aid', 'falls_risk_observed',
        ]
        widgets = {
            'category':             forms.Select(attrs={'class': 'form-select', 'id': 'id_category'}),
            'priority':             forms.Select(attrs={'class': 'form-select'}),
            'note_text':            forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                        'placeholder': 'Enter any additional notes here...'}),
            # Observation
            'obs_location':         forms.Select(attrs={'class': 'form-select'}),
            'obs_status':           forms.Select(attrs={'class': 'form-select'}),
            'obs_completed':        forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # Personal care
            'wash_type':            forms.Select(attrs={'class': 'form-select'}),
            'oral_care':            forms.Select(attrs={'class': 'form-select'}),
            'continence':           forms.Select(attrs={'class': 'form-select'}),
            'pressure_area':        forms.Select(attrs={'class': 'form-select'}),
            'repositioned':         forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'repositioned_position':forms.TextInput(attrs={'class': 'form-control',
                                        'placeholder': 'e.g. Left lateral, Sitting upright'}),
            # Nutrition
            'meal_time':            forms.Select(attrs={'class': 'form-select'}),
            'appetite':             forms.Select(attrs={'class': 'form-select'}),
            'fluid_intake':         forms.Select(attrs={'class': 'form-select'}),
            'fluid_amount_ml':      forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ml'}),
            'weight_kg':            forms.NumberInput(attrs={'class': 'form-control',
                                        'placeholder': 'kg', 'step': '0.1'}),
            # Wellbeing
            'mood':                 forms.Select(attrs={'class': 'form-select'}),
            'sleep_quality':        forms.Select(attrs={'class': 'form-select'}),
            'sleep_hours':          forms.NumberInput(attrs={'class': 'form-control',
                                        'placeholder': 'e.g. 6.5', 'step': '0.5'}),
            # Mobility
            'mobility_aid':         forms.Select(attrs={'class': 'form-select'}),
            'falls_risk_observed':  forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }