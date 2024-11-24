from django.shortcuts import render
from prediction_app.models import Patient, Room
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@permission_classes([IsAuthenticated])
def manage_room(request):
    rooms = Room.objects.all()
    return render(request, 'room_management.html', {'rooms': rooms})