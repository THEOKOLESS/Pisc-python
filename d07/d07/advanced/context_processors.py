from django.contrib.auth.forms import AuthenticationForm


def nav_login_form(request):
    return {'nav_login_form': AuthenticationForm()}
