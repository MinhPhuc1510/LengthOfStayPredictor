from django.shortcuts import render
from prediction_app.models import Patient, Admission
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now


@permission_classes([IsAuthenticated])
def get_patient_info(request, id):
    patient = Patient.objects.filter(id=id).first()
    admissions = Admission.objects.filter(patient=patient)

    for admission in admissions:
        if admission.los_number is not None:
            duaration = (now() - admission.created_time).days
            if duaration >= admission.los_number:
                admission.status = 'D'
            admission.save()

    allow_admission_request = admissions.filter(status="I").count() == 0

    return render(request, 'patient_info.html', {'patient': patient, 'admissions': admissions, "alow_admission_request": allow_admission_request})
