from django.shortcuts import render
from prediction_app.models import Patient, Admission
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now


@permission_classes([IsAuthenticated])
def get_admission_info(request, id, admission_id):
    patient = Patient.objects.get(id=id)
    admission = patient.admission_set.filter(hadm_id=admission_id).first()
    if admission.dischtime:
        duaration = admission.los_number
    else:
        duaration = (now() - admission.admittime).days
    return render(request,'admission_info.html', {'admission': admission, 'patient': patient, 'duaration': duaration})

@permission_classes([IsAuthenticated])
def update_admission_discharged_status(request, id, admission_id):
    patient = Patient.objects.get(id=id)
    admission = patient.admission_set.filter(hadm_id=admission_id).first()
    admission.status = "Discharged"
    admission.dischtime = now()
    admission.save()

    return render(request,'admission_info.html', {'admission': admission, 'patient': patient, 'duaration': admission.los_number})

@permission_classes([IsAuthenticated])
def update_admission_los_label(request, id, admission_id):
    patient = Patient.objects.get(id=id)
    admission = patient.admission_set.filter(hadm_id=admission_id).first()
    duaration = 0
    if request.method == "POST":
        los_label = request.POST.get("los_label")
        print(los_label)
        admission.los_label = los_label
        admission.save()
        print(admission.dischtime)
        if admission.dischtime:
            duaration = admission.los_number
        else:
            duaration = (now() - admission.admittime).days
    return render(request,'admission_info.html', {'admission': admission, 'patient': patient, 'duaration': duaration})
