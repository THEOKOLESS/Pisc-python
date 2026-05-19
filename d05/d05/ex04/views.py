import psycopg2
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

MOVIES_DATA = [
    {'episode_nb': 1, 'title': 'The Phantom Menace', 'director': 'George Lucas', 'producer': 'Rick McCallum', 'release_date': '1999-05-19'},
    {'episode_nb': 2, 'title': 'Attack of the Clones', 'director': 'George Lucas', 'producer': 'Rick McCallum', 'release_date': '2002-05-16'},
    {'episode_nb': 3, 'title': 'Revenge of the Sith', 'director': 'George Lucas', 'producer': 'Rick McCallum', 'release_date': '2005-05-19'},
    {'episode_nb': 4, 'title': 'A New Hope', 'director': 'George Lucas', 'producer': 'Gary Kurtz, Rick McCallum', 'release_date': '1977-05-25'},
    {'episode_nb': 5, 'title': 'The Empire Strikes Back', 'director': 'Irvin Kershner', 'producer': 'Gary Kutz, Rick McCallum', 'release_date': '1980-05-17'},
    {'episode_nb': 6, 'title': 'Return of the Jedi', 'director': 'Richard Marquand', 'producer': 'Howard G. Kazanjian, George Lucas, Rick McCallum', 'release_date': '1983-05-25'},
    {'episode_nb': 7, 'title': 'The Force Awakens', 'director': 'J. J. Abrams', 'producer': 'Kathleen Kennedy, J. J. Abrams, Bryan Burk', 'release_date': '2015-12-11'},
]


def get_connection():
    db = settings.DATABASES['default']
    return psycopg2.connect(
        dbname=db['NAME'],
        user=db['USER'],
        password=db['PASSWORD'],
        host=db['HOST'],
        port=db['PORT'],
    )


def init(request):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ex04_movies (
                episode_nb    INTEGER PRIMARY KEY,
                title         VARCHAR(64) UNIQUE NOT NULL,
                opening_crawl TEXT,
                director      VARCHAR(32) NOT NULL,
                producer      VARCHAR(128) NOT NULL,
                release_date  DATE NOT NULL
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(str(e))


def populate(request):
    lines = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        for data in MOVIES_DATA:
            try:
                cursor.execute("""
                    INSERT INTO ex04_movies (episode_nb, title, opening_crawl, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, (
                    data['episode_nb'],
                    data['title'],
                    None,
                    data['director'],
                    data['producer'],
                    data['release_date'],
                ))
                conn.commit()
                lines.append("OK")
            except Exception as e:
                conn.rollback()
                lines.append(f"{data['title']}: {str(e)}")
        cursor.close()
        conn.close()
    except Exception as e:
        return HttpResponse(str(e))
    return HttpResponse("<br>".join(lines))


def display(request):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT episode_nb, title, opening_crawl, director, producer, release_date FROM ex04_movies;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            return HttpResponse("No data available")
        movies = [
            {
                'episode_nb': row[0],
                'title': row[1],
                'opening_crawl': row[2],
                'director': row[3],
                'producer': row[4],
                'release_date': row[5],
            }
            for row in rows
        ]
        return render(request, 'ex04/display.html', {'movies': movies})
    except Exception:
        return HttpResponse("No data available")


def remove(request):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if request.method == 'POST':
            title = request.POST.get('title')
            cursor.execute("DELETE FROM ex04_movies WHERE title = %s;", (title,))
            conn.commit()
        cursor.execute("SELECT episode_nb, title, opening_crawl, director, producer, release_date FROM ex04_movies;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            return HttpResponse("No data available")
        movies = [
            {
                'episode_nb': row[0],
                'title': row[1],
                'opening_crawl': row[2],
                'director': row[3],
                'producer': row[4],
                'release_date': row[5],
            }
            for row in rows
        ]
        return render(request, 'ex04/remove.html', {'movies': movies})
    except Exception:
        return HttpResponse("No data available")
