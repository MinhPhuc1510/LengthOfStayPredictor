from django import forms
from .models import Patient, Admission

class AddNewPatientForm(forms.ModelForm):
    class Meta:
        model= Patient
        fields = '__all__'

class AddNewAdmission(forms.ModelForm):
    DIAGNOSIS = [
        ('viral_pneumonia', 'Viral Pneumonia'), 
        ('pneumococcal_pneumonia', 'Pneumococcal Pneumonia'), 
        ('bacterial_pneumonia', 'Bacterial Pneumonia'), 
        ('other_specified_organism_pneumonia', 'Other Specified Organism Pneumonia'), 
        ('bronchopneumonia_unspecified', 'Bronchopneumonia Unspecified'),
        ('unspecified_pneumonia', 'Unspecified Pneumonia'),
    ]

    diagnose = forms.MultipleChoiceField(
        choices=DIAGNOSIS,
        widget=forms.SelectMultiple(attrs={
            'id': 'diagnose', 
            'required': True,
        }),
    )
    class Meta:
        model= Admission
        fields = '__all__'


class PatientInfoForm(forms.Form):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    name = forms.CharField(max_length=100, required=True, label="Name")
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, 
        label="Gender", 
        required=True, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    age = forms.IntegerField(
        label="Age", 
        min_value=0, 
        max_value=120, 
        required=True, 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    marital_stautus = forms.CharField(max_length=100, required=True, label="Marital Stautus", widget=forms.TextInput(attrs={'class': 'form-control'}))
    regligon = forms.CharField(max_length=100, required=True, label="Regligon", widget=forms.TextInput(attrs={'class': 'form-control'}))
    ethnicity = forms.CharField(max_length=100, required=True, label="Ethnicity", widget=forms.TextInput(attrs={'class': 'form-control'}))
    admission_type = forms.CharField(max_length=100, required=True, label="Admission Type", widget=forms.TextInput(attrs={'class': 'form-control'}))
    diagnosis = forms.CharField(
        label="Diagnosis", 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None or age < 0:
            raise forms.ValidationError("Age must be a positive number.")
        return age
