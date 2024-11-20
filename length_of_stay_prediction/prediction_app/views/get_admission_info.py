from django.shortcuts import render
from prediction_app.models import Patient
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@permission_classes([IsAuthenticated])
def get_admission_info(request):
    return render(request,'admission_info.html')