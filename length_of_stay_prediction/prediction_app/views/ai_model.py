import pandas as pd
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from prediction_app.models import AIModelStats, Admission
from django.utils.dateformat import DateFormat
from django.db.models import F
from jchart import Chart
from jchart.config import Axes, DataSet
import json
from prediction_app.prediction_model.ml_model import LosModel
from datetime import datetime
# View for AI Model
LOS_LABLE_TO_ID = {
    'Less than 3 days': 0,
    '3-7 days': 1,
    '7-14 days': 2,
    'More than 14 days': 3,
}

class PerformanceChart(Chart):
    chart_type = 'bar'

    def get_datasets(self, **kwargs):
        admissions = Admission.objects.filter(status='Discharged')

        # Categorize records
        cat1_actual = admissions.filter(los_actual_label='Less than 3 days', status='Discharged').count()
        cat2_actual = admissions.filter(los_actual_label='3-7 days', status='Discharged').count()
        cat3_actual = admissions.filter(los_actual_label='7-14 days', status='Discharged').count()
        cat4_actual = admissions.filter(los_actual_label='More than 14 days', status='Discharged').count()


        cat1_predicted = admissions.filter(los_label='Less than 3 days', status='Discharged').count()
        cat2_predicted = admissions.filter(los_label='3-7 days', status='Discharged').count()
        cat3_predicted = admissions.filter(los_label='7-14 days', status='Discharged').count()
        cat4_predicted = admissions.filter(los_label='More than 14 days', status='Discharged').count()

        return [
            DataSet(label="Actual", data=[cat1_actual, cat2_actual, cat3_actual, cat4_actual], backgroundColor="rgba(75, 192, 192, 0.6)"),
            DataSet(label="Predicted", data=[cat1_predicted, cat2_predicted, cat3_predicted, cat4_predicted], backgroundColor="rgba(153, 102, 255, 0.6)")
        ]

    def get_axes(self, **kwargs):
        return [
            Axes(type='category', labels=['Less than 3 days', '3-7 days', '7-14 days', '14+ days']),
            Axes(type='linear', position='left')
        ]

def ai_model_view(request):
    try:
        # Calculate accuracy based on Admission records
        total_discharged = Admission.objects.filter(status='Discharged').count()
        correct_label_predictions = Admission.objects.filter(status='Discharged').filter(los_label=F('los_actual_label')).count()
        accuracy = (correct_label_predictions / total_discharged) * 100 if total_discharged > 0 else None
        formatted_accuracy = f"{accuracy:.2f}" if accuracy is not None else "N/A"
        # Number of samples is the number of discharged records
        num_samples = total_discharged

        # Fetch the latest AIModelStats record
        latest_stats = AIModelStats.objects.latest('last_training_time')

        # Calculate accuracy change
        previous_stats = AIModelStats.objects.filter(id__lt=latest_stats.id).order_by('-id').first()
        accuracy_change = (accuracy - previous_stats.accuracy * 100) if previous_stats and accuracy is not None else None
        
        # Determine the color and format for accuracy change
        if accuracy_change is not None:
            if accuracy_change > 0:
                accuracy_change_display = f"+{accuracy_change:.2f}%"
                change_color = "green"
            else:
                accuracy_change_display = f"{accuracy_change:.2f}%"
                change_color = "red"
        else:
            accuracy_change_display = "N/A"
            change_color = "black"

        # Format the last training time
        formatted_last_training_time = DateFormat(latest_stats.last_training_time).format('Y-m-d H:i:s')

        performance_chart = PerformanceChart()

        # Serialize the chart data to JSON
        chart_data = json.dumps(performance_chart.get_datasets())

        context = {
            'accuracy': accuracy,
            'formatted_accuracy': formatted_accuracy,
            'accuracy_change': accuracy_change_display,
            'change_color': change_color,
            'num_samples': num_samples,
            'last_training_time': formatted_last_training_time,
            'chart_data': chart_data  # Pass the serialized chart data to the template
        }
    except AIModelStats.DoesNotExist:
        # If no stats exist, provide default values
        context = {
            'accuracy': 'N/A',
            'formatted_accuracy': 'N/A',
            'accuracy_change': 'N/A',
            'change_color': 'black',
            'num_samples': 'N/A',
            'last_training_time': 'N/A',
            'chart_data': json.dumps([])  # Pass an empty list as default chart data
        }
    return render(request, 'ai_model.html', context)

# Endpoint to handle file upload for re-training

def retrain_model(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Query Admission records based on discharge date within the specified range
        admissions = Admission.objects.filter(dischtime__range=[start_date, end_date]).select_related('subject')

        if not admissions.exists():
            return JsonResponse({'error': 'No records found for the selected date range.'})

        # Prepare the data for training
        data = []
        label = []
        for admission in admissions:
            patient = admission.subject
            data.append({
                "TEXT": admission.clinical_note,
                "DIAGNOSIS": admission.diagnose,
                "GENDER": patient.gender,
                "ADMISSION_TYPE": admission.admission_type,
                "INSURANCE": admission.insurance,
                "RELIGION": patient.religion,
                "ETHNICITY": patient.ethnicity,
                "MARITAL_STATUS": patient.marital_status,
                "AGE": patient.age,
                "FIRST_CAREUNIT": "ICU"
            })
            label.append(LOS_LABLE_TO_ID[admission.los_actual_label])

        df = pd.DataFrame(data)
        # df_label = pd.DataFrame(label)
        y = np.array(label)
        # Instantiate the model and train it
        los_model = LosModel().load_model()
        los_model.train(df, y)  
        los_model.approve_model() 

        # Calculate accuracy
        total_discharged = Admission.objects.filter(status='Discharged').count()
        correct_label_predictions = Admission.objects.filter(status='Discharged').filter(los_label=F('los_actual_label')).count()
        accuracy = (correct_label_predictions / total_discharged) * 100 if total_discharged > 0 else None
        num_samples = total_discharged

        # Update the latest AIModelStats record
        latest_stats = AIModelStats.objects.latest('id')
        latest_stats.accuracy = accuracy / 100
        latest_stats.num_samples = num_samples
        latest_stats.save()

        # Insert a new record in AIModelStats
        AIModelStats.objects.create(
            last_training_time=datetime.now()  # Ensure to import datetime
        )
        return JsonResponse({'success': 'Model retrained successfully.'})