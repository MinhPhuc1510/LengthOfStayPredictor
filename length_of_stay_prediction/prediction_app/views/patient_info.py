from django.shortcuts import render
from prediction_app.models import Patient, Admission
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@permission_classes([IsAuthenticated])
def get_patient_info(request, id):
    patient = Patient.objects.filter(id=id).first()
    admission = Admission.objects.filter(patient=patient)
    return render(request, 'patient_info.html', {'patient': patient, 'admissions': admission})