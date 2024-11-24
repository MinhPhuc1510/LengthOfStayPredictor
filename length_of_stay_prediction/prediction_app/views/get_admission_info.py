from django.shortcuts import render
from prediction_app.models import Patient, Admission
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@permission_classes([IsAuthenticated])
def get_admission_info(request, id, admission_id):
    patient = Patient.objects.get(id=id)
    admission = patient.admission_set.filter(id=admission_id).first()
    return render(request,'admission_info.html', {'admission': admission, 'patient': patient})