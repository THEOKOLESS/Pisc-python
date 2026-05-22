from django.http import HttpResponse
from django.shortcuts import render
from .models import People


def display(request):
    try:
        people = People.objects.filter(
            homeworld__climate__contains='windy'
        ).select_related('homeworld').order_by('name')
        if not people.exists():
            return HttpResponse(
                "No data available, please use the following command line before use:<br>"
                "python3 manage.py appenddata ex09/ex09_initial_data.json"
            )
        return render(request, 'ex09/display.html', {'people': people})
    except Exception:
        return HttpResponse(
            "No data available, please use the following command line before use:<br>"
            "python3 manage.py appenddata ex09/ex09_initial_data.json"
        )
