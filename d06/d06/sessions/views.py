import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.conf import settings
from django.utils import timezone
from .forms import RegisterForm, LoginForm, TipForm
from .models import Tip


def welcome(request):
    now = timezone.now().timestamp()
    expires_at = request.session.get('username_expires_at', 0)

    if now >= expires_at:
        request.session['username'] = random.choice(settings.USERNAMES)
        request.session['username_expires_at'] = now + settings.USERNAME_DURATION

    form = None
    if request.user.is_authenticated:
        form = TipForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            tip = form.save(commit=False)
            tip.author = request.user
            tip.save()
            return redirect('welcome')

    tips = Tip.objects.select_related('author').all()
    return render(request, 'welcome/welcome.html', {
        'anon_username': request.session['username'],
        'form': form,
        'tips': tips,
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('welcome')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = get_user_model().objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        login(request, user)
        return redirect('welcome')

    return render(request, 'welcome/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('welcome')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user is not None:
            login(request, user)
            return redirect('welcome')
        form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'welcome/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('welcome')