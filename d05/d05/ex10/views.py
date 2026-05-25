import json
import os
from django.shortcuts import render
from django.conf import settings
from .models import Planets, People, Movies


def load_data():
    fixture_path = os.path.join(settings.BASE_DIR, 'ex10', 'ex10_initial_data.json')
    try:
        with open(fixture_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise Exception(f"Fixture file not found: {fixture_path}")


    pk_to_planet = {}
    for entry in data:
        if entry['model'] == 'ex10.planets':
            f = entry['fields']
            planet, _ = Planets.objects.get_or_create(
                name=f['name'],
                defaults={
                    'climate': f.get('climate'),
                    'diameter': f.get('diameter'),
                    'orbital_period': f.get('orbital_period'),
                    'population': f.get('population'),
                    'rotation_period': f.get('rotation_period'),
                    'surface_water': f.get('surface_water'),
                    'terrain': f.get('terrain'),
                }
            )
            pk_to_planet[entry['pk']] = planet

    pk_to_person = {}
    for entry in data:
        if entry['model'] == 'ex10.people':
            f = entry['fields']
            planet = pk_to_planet.get(f.get('homeworld'))
            person, _ = People.objects.get_or_create(
                name=f['name'],
                defaults={
                    'birth_year': f.get('birth_year'),
                    'gender': f.get('gender'),
                    'eye_color': f.get('eye_color'),
                    'hair_color': f.get('hair_color'),
                    'height': f.get('height'),
                    'mass': f.get('mass'),
                    'homeworld': planet,
                }
            )
            pk_to_person[entry['pk']] = person

    for entry in data:
        if entry['model'] == 'ex10.movies':
            f = entry['fields']
            movie, _ = Movies.objects.get_or_create(
                episode_nb=entry['pk'],
                defaults={
                    'title': f['title'],
                    'opening_crawl': f.get('opening_crawl'),
                    'director': f['director'],
                    'producer': f['producer'],
                    'release_date': f['release_date'],
                }
            )
            for char_pk in f.get('characters', []):
                person = pk_to_person.get(char_pk)
                if person:
                    movie.characters.add(person)


def display(request):
    from django.http import HttpResponse
    if not Movies.objects.exists():
        try:
            load_data()
        except Exception as e:
            return HttpResponse(str(e))

    genders = People.objects.values_list('gender', flat=True).distinct().order_by('gender')

    results = None
    if request.method == 'POST':
        min_date = request.POST.get('min_date')
        max_date = request.POST.get('max_date')
        min_diameter = request.POST.get('min_diameter')
        gender = request.POST.get('gender')

        results = People.objects.filter(
            gender=gender,
            homeworld__diameter__gte=min_diameter,
            movies__release_date__gte=min_date,
            movies__release_date__lte=max_date,
        ).select_related('homeworld').prefetch_related('movies').values(
            'name',
            'gender',
            'homeworld__name',
            'homeworld__diameter',
            'movies__title',
        ).order_by('movies__title', 'name')

        if not results:
            results = []

    return render(request, 'ex10/display.html', {
        'genders': genders,
        'results': results,
    })
