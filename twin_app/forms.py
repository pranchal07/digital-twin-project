from django import forms
from .models import HealthData, UserProfile

class HealthDataForm(forms.ModelForm):
    class Meta:
        model = HealthData
        exclude = ['user', 'timestamp']
        widgets = {
            'heart_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter heart rate (60-100 bpm)',
                'min': 40,
                'max': 200
            }),
            'bp_systolic': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter systolic pressure (90-120 mmHg)',
                'min': 70,
                'max': 200
            }),
            'bp_diastolic': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter diastolic pressure (60-80 mmHg)',
                'min': 40,
                'max': 120
            }),
            'temperature': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter temperature (98.6°F)',
                'min': 95,
                'max': 105,
                'step': 0.1
            }),
            'spo2': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter oxygen saturation (95-100%)',
                'min': 70,
                'max': 100
            }),
            'sleep_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sleep hours (7-9 hours)',
                'min': 0,
                'max': 24,
                'step': 0.5
            }),
            'stress_level': forms.NumberInput(attrs={
                'class': 'form-range',
                'type': 'range',
                'min': 1,
                'max': 10,
                'value': 5
            }),
            'diet_quality': forms.NumberInput(attrs={
                'class': 'form-range',
                'type': 'range',
                'min': 1,
                'max': 10,
                'value': 5
            }),
            'water_intake': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter water intake (8 glasses)',
                'min': 0,
                'max': 20
            }),
            'physical_activity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter activity hours (1-2 hours)',
                'min': 0,
                'max': 10,
                'step': 0.5
            }),
            'study_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter study hours per day',
                'min': 0,
                'max': 16,
                'step': 0.5
            }),
            'attendance': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter attendance percentage',
                'min': 0,
                'max': 100
            }),
            'assignments_completed': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter assignment completion percentage',
                'min': 0,
                'max': 100
            }),
            'focus_level': forms.NumberInput(attrs={
                'class': 'form-range',
                'type': 'range',
                'min': 1,
                'max': 10,
                'value': 5
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'created_at', 'updated_at']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 120}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height in cm'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight in kg'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
        }
