from django.shortcuts import render
from prediction_app.models import Patient
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from prediction_app.forms import AddNewAdmission
from django.contrib import messages
import logging

@permission_classes([IsAuthenticated])
def add_new_admission(request, id):
    patient = Patient.objects.get(id=id)
    
    if request.method == 'POST':
        data = request.POST.copy()
        data['patient'] = patient
        print(data)

        form = AddNewAdmission(data)
        print(form.errors)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Sent admission request Successfully!')
            except:
                logging.error('Error saving')
                return render(request, 'add_new_admission.html', {'error_message': 'Error saving', 'patient':patient})
        else:
            return render(request, 'add_new_admission.html', {'form': form, 'error_message': 'Invalid input.', 'patient':patient})
    elif request.method == 'GET':
        return render(request, 'add_new_admission.html', {'form': AddNewAdmission(), 'patient':patient})
    return render(request, 'add_new_admission.html', {'form': AddNewAdmission(), 'patient':patient})
 