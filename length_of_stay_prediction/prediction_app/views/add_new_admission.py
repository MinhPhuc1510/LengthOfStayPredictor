from django.shortcuts import render
from prediction_app.models import Patient, Room, Admission
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from prediction_app.forms import AddNewAdmission
from django.contrib import messages
from django.db.models import Q, Count, F
import logging

@permission_classes([IsAuthenticated])
def add_new_admission(request, id):
    patient = Patient.objects.get(id=id)
    patient_in_treatment = Count("admission", filter=Q(admission__status="In Treatment"))
    rooms = Room.objects.annotate(num_patients=patient_in_treatment).filter(num_patients__lt=F("max_beds"))
    
    if request.method == 'POST':
        data = request.POST.copy()
        data['subject'] = patient
        # print(data)

        form = AddNewAdmission(data)
        # print(form.errors)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Sent admission request Successfully!')
            except Exception as e:
                logging.error(f'Error saving: {e}')
                return render(request, 'add_new_admission.html', {'error_message': 'Error saving', 'patient':patient, "rooms": rooms, 'form': form})
        else:
            return render(request, 'add_new_admission.html', {'form': form, 'error_message': 'Invalid input.', 'patient':patient, "rooms": rooms})
    elif request.method == 'GET':
        return render(request, 'add_new_admission.html', {'form': AddNewAdmission(), 'patient':patient, "rooms": rooms})
    return render(request, 'add_new_admission.html', {'form': AddNewAdmission(), 'patient':patient, "rooms": rooms})
 