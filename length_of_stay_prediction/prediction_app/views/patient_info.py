from django.shortcuts import render
from prediction_app.models import Patient, Admission
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import F, ExpressionWrapper, DurationField
from django.utils.timezone import now
from datetime import timedelta


@permission_classes([IsAuthenticated])
def get_patient_info(request, id):
    patient = Patient.objects.filter(id=id).first()
    admissions = Admission.objects.filter(patient=patient).order_by("created_time")

    for admission in admissions:
        if admission.los_number is not None:
            duaration = (now() - admission.created_time).days
            if duaration >= admission.los_number:
                admission.status = 'D'
            else:
                admission.status = 'I'
            admission.save()

    alow_admission_request = admissions.filter(status="I").count() == 0

    return render(request, 'patient_info.html', {'patient': patient, 'admissions': admissions, "alow_admission_request": alow_admission_request})
