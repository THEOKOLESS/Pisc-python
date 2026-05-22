import json
from django.core.management.base import BaseCommand
from ex09.models import Planets, People


class Command(BaseCommand):
    help = 'Load ex09 fixture resolving homeworld pk to planet name'

    def add_arguments(self, parser):
        parser.add_argument('fixture', type=str)

    def handle(self, *args, **options):
        with open(options['fixture'], 'r') as f:
            data = json.load(f)

        pk_to_name = {
            entry['pk']: entry['fields']['name']
            for entry in data
            if entry['model'] == 'ex09.planets'
        }

        for entry in data:
            if entry['model'] == 'ex09.planets':
                f = entry['fields']
                Planets.objects.get_or_create(
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

        for entry in data:
            if entry['model'] == 'ex09.people':
                f = entry['fields']
                hw_pk = f.get('homeworld')
                planet = None
                if hw_pk is not None:
                    planet = Planets.objects.filter(name=pk_to_name[hw_pk]).first()
                People.objects.get_or_create(
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

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
