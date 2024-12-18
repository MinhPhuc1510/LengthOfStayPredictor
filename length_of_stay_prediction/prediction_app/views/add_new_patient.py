import django
from django.shortcuts import render
from prediction_app.forms import AddNewPatientForm
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from ..models import User
from django.contrib.auth.hashers import make_password


import logging
from datetime import datetime


@permission_classes([IsAuthenticated])
def create_patient(request):
    if request.method == 'POST':
        data = request.POST.copy()
        # print(data)
        dob = data.get("date_of_birth")
        if dob:
            # Calculate the age from the date of birth
            dob = datetime.strptime(dob, "%Y-%m-%d")
            today = datetime.today()
            calculated_age = today.year - dob.year - \
                ((today.month, today.day) < (dob.month, dob.day))
            data['age'] = calculated_age
        
        try:
            user = User.objects.create(**{
                "username": f'{data["first_name"]} {data["last_name"]}',
                "role": "patient",
                "date_of_birth": dob,
                "is_active": True,
                "password": make_password(f'{data["first_name"]} {data["last_name"]}')
            })
        except django.db.utils.IntegrityError:
            logging.error('user is already registered')
            return render(request, 'add_new_patient.html', {'error_message': 'user is already registered'})
        data['user'] = user

        form = AddNewPatientForm(data)
        # print(form.errors)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Created Patient Successfully!')
            except:
                logging.error('Error saving')
                return render(request, 'add_new_patient.html', {'error_message': 'Error saving'})
        else:
            return render(request, 'add_new_patient.html', {'form': form, 'error_message': 'Invalid input.'})
    elif request.method == 'GET':
        return render(request, 'add_new_patient.html', {'form': AddNewPatientForm()})
    return render(request, 'add_new_patient.html', {'form': AddNewPatientForm()})
