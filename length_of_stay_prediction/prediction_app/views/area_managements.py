from django.shortcuts import render
from prediction_app.models import Area
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, F, ExpressionWrapper, IntegerField, Sum


@permission_classes([IsAuthenticated])
def manage_area(request):
    areas = Area.objects.all()
    patient_in_treatment = Count("admission", filter=Q(admission__status="I"))
    results = []

    for area in areas:
        rooms = area.room_set.annotate(num_patients=patient_in_treatment).annotate(percentage=ExpressionWrapper(
            F("num_patients") * 100.0 / F("max_beds"),
            output_field=IntegerField()
        ))
        totals = rooms.aggregate(
            total_num_patients=Sum('num_patients'),
            total_max_beds=Sum('max_beds')
        )

        total_num_patients = totals['total_num_patients']
        total_max_beds = totals['total_max_beds']

        if total_max_beds > 0:
            occupancy_rate = (total_num_patients / total_max_beds) * 100
        else:
            occupancy_rate = 0

        results.append({
            'area': area.name,
            'rooms': rooms,
            'lor': len(rooms),
            'sum_percentage': occupancy_rate,
            "total_max_beds": total_max_beds,
            "total_num_patients": total_num_patients
        })
    return render(request, 'area_management.html', {'results': results})
