# prediction_app/urls.py

from django.urls import path
from prediction_app.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', user_login),
    # path('predict-los', predict_length_of_stay,
    #      name='predict_length_of_stay'),  # Main prediction view
    path('login', user_login, name='user_login'),
    path('logout', user_logout, name='user_out'),
    path('patients/create', create_patient, name='create_new_patient'),
    path('patients', get_patients, name='get_patients'),
    path('patients/<int:id>', get_patient_info, name='get_patient_info'),
    path('patients/<int:id>/admission_info/<int:admission_id>', get_admission_info, name='get_admission_info'),
    path('patients/<int:id>/admission_info/create', add_new_admission, name='add_new_admission'),
     path('rooms', manage_room, name='manage_room'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
