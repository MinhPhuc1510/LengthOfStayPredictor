from django import forms

class PatientInfoForm(forms.Form):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, label="Gender")
    age = forms.IntegerField(min_value=0, max_value=120, required=True, label="Age")
    illness = forms.CharField(max_length=100, required=True, label="Illness")

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None or age < 0:
            raise forms.ValidationError("Age must be a positive number.")
        return age
