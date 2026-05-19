from django.http import HttpResponse
import psycopg2
from django.conf import settings

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
        conn= get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ex00_movies (
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
  