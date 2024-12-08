from django import forms
from .models import Patient, Admission

class AddNewPatientForm(forms.ModelForm):
    class Meta:
        model= Patient
        fields = '__all__'

class AddNewAdmission(forms.ModelForm):
    ICD_CODE = [
        (0, ' infectious and parasitic diseases'),
        (1, ' neoplasms'),
        (2, ' endocrine, nutritional and metabolic diseases, and immunity disorders'),
        (3, ' diseases of the blood and blood-forming organs'),
        (4, ' mental disorders'),
        (5, ' diseases of the nervous system and sense organs'),
        (6, ' diseases of the circulatory system'),
        (7, ' diseases of the respiratory system'),
        (8, ' diseases of the digestive system'),
        (9, ' diseases of the genitourinary system'),
        (10, ' complications of pregnancy, childbirth, and the puerperium'),
        (11, ' diseases of the skin and subcutaneous tissue'),
        (12, ' diseases of the musculoskeletal system and connective tissue'),
        (13, ' congenital anomalies'),
        (14, ' certain conditions originating in the perinatal period'),
        (15, ' symptoms, signs, and ill-defined conditions'),
        (16, ' injury and poisoning'),
    ]

    icd_code = forms.MultipleChoiceField(
        choices=ICD_CODE,
        widget=forms.SelectMultiple(attrs={
            'id': 'icd_code', 
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
