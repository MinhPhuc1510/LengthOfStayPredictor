from django.shortcuts import render
from prediction_app.models import Patient
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@permission_classes([IsAuthenticated])
def get_patients(request):
    patients = Patient.objects.all()
    return render(request, 'patients.html', {'patients': patients})