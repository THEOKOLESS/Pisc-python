import os
import psycopg2
from django.http import HttpResponse
from django.shortcuts import render

from django.conf import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


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
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ex08_planets (
                id              SERIAL PRIMARY KEY,
                name            VARCHAR(64) UNIQUE NOT NULL,
                climate         VARCHAR,
                diameter        INTEGER,
                orbital_period  INTEGER,
                population      BIGINT,
                rotation_period INTEGER,
                surface_water   REAL,
                terrain         VARCHAR(128)
            );
            CREATE TABLE IF NOT EXISTS ex08_people (
                id          SERIAL PRIMARY KEY,
                name        VARCHAR(64) UNIQUE NOT NULL,
                birth_year  VARCHAR(32),
                gender      VARCHAR(32),
                eye_color   VARCHAR(32),
                hair_color  VARCHAR(32),
                height      INTEGER,
                mass        REAL,
                homeworld   VARCHAR(64) REFERENCES ex08_planets(name)
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
    for filename, table, columns in [
        ('planets.csv', 'ex08_planets', ('name', 'climate', 'diameter', 'orbital_period', 'population', 'rotation_period', 'surface_water', 'terrain')),
        ('people.csv',  'ex08_people',  ('name', 'birth_year', 'gender', 'eye_color', 'hair_color', 'height', 'mass', 'homeworld')),
    ]:
        try:
            conn = get_connection()
            cur = conn.cursor()
            with open(os.path.join(BASE_DIR, filename), 'r') as f:
                cur.copy_from(f, table, sep='\t', null='NULL', columns=columns)
            conn.commit()
            cur.close()
            conn.close()
            lines.append("OK")
        except Exception as e:
            lines.append(str(e))
    return HttpResponse("<br>".join(lines))


def display(request):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT people.name, planets.name, planets.climate
            FROM ex08_people AS people
            JOIN ex08_planets AS planets ON people.homeworld = planets.name
            WHERE planets.climate LIKE '%windy%'
            ORDER BY people.name ASC;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        if not rows:
            return HttpResponse("No data available")
        return render(request, 'ex08/display.html', {'rows': rows})
    except Exception:
        return HttpResponse("No data available")
