# prediction_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_length_of_stay, name='predict_length_of_stay'),  # Main prediction view
]
