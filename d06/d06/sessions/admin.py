from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Tip, User

admin.site.register(Tip)
admin.site.register(User, UserAdmin)
