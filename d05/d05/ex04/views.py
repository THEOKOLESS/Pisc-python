from django.http import HttpResponse
import psycopg2
from django.shortcuts import render
from django.http import HttpResponse

from .models import Movies
# Create your views here.

MOVIES_DATA = [
    {'episode_nb': 1, 'title': 'The Phantom Menace', 'director': 'George Lucas', 'producer': 'Rick McCallum', 'release_date': '1999-05-19'},
    {'episode_nb': 2, 'title': 'Attack of the Clones', 'director': 'George Lucas', 'producer': 'Rick McCallum', 'release_date': '2002-05-16'},
    {'episode_nb': 3, 'title': 'Revenge of the Sith', 'director': 'George Lucas', 'producer': 'Rick McCallum', 'release_date': '2005-05-19'},
    {'episode_nb': 4, 'title': 'A New Hope', 'director': 'George Lucas', 'producer': 'Gary Kurtz, Rick McCallum', 'release_date': '1977-05-25'},
    {'episode_nb': 5, 'title': 'The Empire Strikes Back', 'director': 'Irvin Kershner', 'producer': 'Gary Kutz, Rick McCallum', 'release_date': '1980-05-17'},
    {'episode_nb': 6, 'title': 'Return of the Jedi', 'director': 'Richard Marquand', 'producer': 'Howard G. Kazanjian, George Lucas, Rick McCallum', 'release_date': '1983-05-25'},
    {'episode_nb': 7, 'title': 'The Force Awakens', 'director': 'J. J. Abrams', 'producer': 'Kathleen Kennedy, J. J. Abrams, Bryan Burk', 'release_date': '2015-12-11'},
]


def init(request):
    try:
        conn = psycopg2.connect(
            dbname="formationdjango",
            user="djangouser",
            password="secret",
            host="localhost",
            port="5432",
        )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ex04_movies (
                title       VARCHAR(64) UNIQUE NOT NULL,
                episode_nb  INTEGER PRIMARY KEY,
                opening_crawl TEXT,
                director    VARCHAR(32) NOT NULL,
                producer    VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(str(e))
    
def populate(request):
    lines = []
    for data in MOVIES_DATA:
        try:
            Movies.objects.get_or_create(episode_nb=data['episode_nb'], defaults=data)
            lines.append("OK")
        except Exception as e:
            lines.append(f"{data['title']}: {str(e)}")
    return HttpResponse("<br>".join(lines))



def display(request):
    try:
        movies = Movies.objects.all()
        if not movies.exists():
            return HttpResponse("No data available")
        return render(request, 'ex04/display.html', {'movies': movies})
    except Exception:
        return HttpResponse("No data available")


def remove(request):
    try:
        if request.method == 'POST':
            title = request.POST.get('title')
            Movies.objects.filter(title=title).delete()
        movies = Movies.objects.all()
        if not movies.exists():
            return HttpResponse("No data available")
        return render(request, 'ex04/remove.html', {'movies': movies})
    except Exception:
        return HttpResponse("No data available")