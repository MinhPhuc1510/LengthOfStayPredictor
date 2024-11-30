from django.shortcuts import render
from prediction_app.models import Patient, Room, Area 
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@permission_classes([IsAuthenticated])
def manage_area(request):
    areas = Area.objects.all()
    return render(request, 'area_management.html', {'areas': areas})