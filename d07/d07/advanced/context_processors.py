from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import TextInput, PasswordInput
from django.utils.translation import get_language, gettext as _
from django.urls import translate_url


def nav_login_form(request):
    form = AuthenticationForm()
    form.fields['username'].widget = TextInput(attrs={'class': 'form-control', 'placeholder': _('username')})
    form.fields['password'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': _('password')})
    return {'nav_login_form': form}


def language_switcher(request):
    current_lang = get_language() or 'en'
    if current_lang.startswith('fr'):
        other_lang = 'en'
        label = 'Switch to English'
    else:
        other_lang = 'fr'
        label = 'Passer en français'
    return {
        'other_lang_url': translate_url(request.path, other_lang),
        'other_lang_label': label,
    }
