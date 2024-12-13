from django.shortcuts import render
from django.http import JsonResponse
from prediction_app.models import AIModelStats, Admission
from django.utils.dateformat import DateFormat
from django.db.models import F
from jchart import Chart
from jchart.config import Axes, DataSet
import json

# View for AI Model

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
            'accuracy_change': 'N/A',
            'change_color': 'black',
            'num_samples': 'N/A',
            'last_training_time': 'N/A',
            'chart_data': json.dumps([])  # Pass an empty list as default chart data
        }
    return render(request, 'ai_model.html', context)

# Endpoint to handle file upload for re-training

def retrain_model(request):
    if request.method == 'POST' and request.FILES['trainingFile']:
        training_file = request.FILES['trainingFile']
        # Handle file upload and initiate re-training
        # For now, just return a success response
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})
