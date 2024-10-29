from django.shortcuts import render
from .forms import PatientInfoForm
#from .prediction_model.predictor import Predictor

def predict_length_of_stay(request):
    result = None
    if request.method == 'POST':
        form = PatientInfoForm(request.POST)
        if form.is_valid():
            # Extract cleaned data
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']
            illness = form.cleaned_data['illness']

            # Run prediction
            #predictor = Predictor()
            #result = predictor.predict([gender, age, illness])[0]
            result = {"result": "Short Term"}
    else:
        form = PatientInfoForm()

    return render(request, r'index.html', {'form': form, 'result': result})
