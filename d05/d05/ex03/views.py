from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from .models import Movies

MOVIES_DATA = [
    {'episode_nb': 1, 'title': 'The Phantom Menace', 'director': 'George Lucas', 'producer': 'Rick McCallum', 'release_date': '1999-05-19'},
    {'episode_nb': 2, 'title': 'Attack of the Clones', 'director': 'George Lucas', 'producer': 'Rick McCallum', 'release_date': '2002-05-16'},
    {'episode_nb': 3, 'title': 'Revenge of the Sith', 'director': 'George Lucas', 'producer': 'Rick McCallum', 'release_date': '2005-05-19'},
    {'episode_nb': 4, 'title': 'A New Hope', 'director': 'George Lucas', 'producer': 'Gary Kurtz, Rick McCallum', 'release_date': '1977-05-25'},
    {'episode_nb': 5, 'title': 'The Empire Strikes Back', 'director': 'Irvin Kershner', 'producer': 'Gary Kutz, Rick McCallum', 'release_date': '1980-05-17'},
    {'episode_nb': 6, 'title': 'Return of the Jedi', 'director': 'Richard Marquand', 'producer': 'Howard G. Kazanjian, George Lucas, Rick McCallum', 'release_date': '1983-05-25'},
    {'episode_nb': 7, 'title': 'The Force Awakens', 'director': 'J. J. Abrams', 'producer': 'Kathleen Kennedy, J. J. Abrams, Bryan Burk', 'release_date': '2015-12-11'},
]


def populate(request):
    try:
        if Movies._meta.db_table not in connection.introspection.table_names():
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(Movies)
    except Exception as e:
        return HttpResponse(str(e))

    lines = []
    for data in MOVIES_DATA:
        try:
            Movies.objects.get_or_create(episode_nb=data['episode_nb'], defaults=data)
            lines.append("OK")
        except Exception as e:
            lines.append(str(e))
    return HttpResponse("<br>".join(lines))


def display(request):
    try:
        movies = Movies.objects.all()
        if not movies.exists():
            return HttpResponse("No data available")
        return render(request, 'ex03/display.html', {'movies': movies})
    except Exception:
        return HttpResponse("No data available")
