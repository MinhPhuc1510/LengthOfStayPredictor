from django.shortcuts import render
from django.http import JsonResponse
from prediction_app.models import AIModelStats
from django.utils.dateformat import DateFormat

# View for AI Model

def ai_model_view(request):
    try:
        # Fetch the latest stats from the database
        latest_stats = AIModelStats.objects.latest('last_training_time')
        previous_stats = AIModelStats.objects.filter(id__lt=latest_stats.id).order_by('-id').first()
        accuracy_change = latest_stats.accuracy - previous_stats.accuracy if previous_stats else 0
        
        # Determine the color and format for accuracy change
        if accuracy_change > 0:
            accuracy_change_display = f"+{accuracy_change*100:.2f}%"
            change_color = "green"
        else:
            accuracy_change_display = f"{accuracy_change*100:.2f}%"
            change_color = "red"

        formatted_last_training_time = DateFormat(latest_stats.last_training_time).format('Y-m-d H:i:s')
        context = {
            'accuracy': latest_stats.accuracy * 100,
            'accuracy_change': accuracy_change_display,
            'change_color': change_color,
            'num_samples': latest_stats.num_samples,
            'last_training_time': formatted_last_training_time,
        }
    except AIModelStats.DoesNotExist:
        # If no stats exist, provide default values
        context = {
            'accuracy': 'N/A',
            'accuracy_change': 'N/A',
            'num_samples': 'N/A',
            'last_training_time': 'N/A',
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
