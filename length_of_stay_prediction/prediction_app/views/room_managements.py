from django.shortcuts import render
from prediction_app.models import Room
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, F, ExpressionWrapper, IntegerField, Sum, FloatField
from django.utils.timezone import now

@permission_classes([IsAuthenticated])
def manage_room(request, id):
    room = Room.objects.filter(id=id)
    patient_in_treatment = Count("admission", filter=Q(admission__status="I"))

    room = room.annotate(num_patients=patient_in_treatment).annotate(percentage=ExpressionWrapper(
        F("num_patients") * 100.0 / F("max_beds"),
        output_field=IntegerField()
    ))
    totals = room.aggregate(
        total_num_patients=Sum('num_patients'),
        total_max_beds=Sum('max_beds')
    )

    total_num_patients = totals['total_num_patients']
    total_max_beds = totals['total_max_beds']

    if total_max_beds > 0:
        occupancy_rate = (total_num_patients / total_max_beds) * 100
    else:
        occupancy_rate = 0

    admissions =  room.first().admission_set.filter(status="I")
    admissions_results = []
    for admission in admissions:
        duaration = (now() - admission.created_time).days
        percentage = int((duaration / admission.los_number) * 100)
        admissions_results.append({
            "admission": admission,
            "percentage": percentage
        })

    result = {
        'room': room.first(),
        'sum_percentage': occupancy_rate,
        "total_max_beds": total_max_beds,
        "total_num_patients": total_num_patients,
        "admissions": admissions_results
    }
    print(result)

    return render(request, 'room_management.html', {'result': result})
