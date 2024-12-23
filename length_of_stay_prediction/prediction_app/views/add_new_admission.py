from django.shortcuts import render
from prediction_app.models import Patient, Room, Admission
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from prediction_app.forms import AddNewAdmission
from django.contrib import messages
from django.db.models import Q, Count, F
from django.http import HttpResponseRedirect
from django.urls import reverse
from prediction_app.prediction_model.ml_model import LosModel
import pandas as pd
import logging

@permission_classes([IsAuthenticated])
def add_new_admission(request, id):
    LOS_ID_TO_LABEL = {
        0: 'Less than 3 days',
        1: '3-7 days',
        2: '7-14 days',
        3: 'More than 14 days'
    }
    patient = Patient.objects.get(id=id)
    patient_in_treatment = Count("admission", filter=Q(admission__status="In Treatment"))
    rooms = Room.objects.annotate(num_patients=patient_in_treatment).filter(num_patients__lt=F("max_beds"))
    
    if request.method == 'POST':
        data = request.POST.copy()
        data['subject'] = patient
        # print(data)

        form = AddNewAdmission(data)
        print(form.errors)
        if form.is_valid():
            try:
                admission = form.save()
                messages.success(request, 'Sent admission request Successfully!')
                X = {
                    "TEXT": admission.clinical_note,
                    "DIAGNOSIS": admission.diagnose,
                    "GENDER": patient.gender,
                    "ADMISSION_TYPE": admission.admission_type,
                    "INSURANCE": admission.insurance,
                    "RELIGION": patient.religion,
                    "ETHNICITY": patient.ethnicity,
                    "MARITAL_STATUS": patient.marital_status,
                    "AGE": patient.age,
                    "FIRST_CAREUNIT": admission.first_careunit  # Assuming default value
                }
                X_input = pd.Series(X)
                los_model = LosModel()
                predicted_los_label = los_model.predict(X_input)
                admission.los_label = LOS_ID_TO_LABEL[predicted_los_label[0]]
                # admission.los_label = "7-14 days"
                admission.save()
                return HttpResponseRedirect(reverse('get_admission_info', args=[id, admission.hadm_id]))
            except Exception as e:
                logging.error(f'Error saving: {e}')
                return render(request, 'add_new_admission.html', {'error_message': 'Error saving', 'patient':patient, "rooms": rooms, 'form': form})
        else:
            return render(request, 'add_new_admission.html', {'form': form, 'error_message': 'Invalid input.', 'patient':patient, "rooms": rooms})
    elif request.method == 'GET':
        return render(request, 'add_new_admission.html', {'form': AddNewAdmission(), 'patient':patient, "rooms": rooms})
    return render(request, 'add_new_admission.html', {'form': AddNewAdmission(), 'patient':patient, "rooms": rooms})
 