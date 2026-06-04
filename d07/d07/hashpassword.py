from django.contrib.auth.hashers import make_password
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'd07.settings'
django.setup()
print(make_password('password123'))