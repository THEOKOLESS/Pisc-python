from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST


def account(request):
    form = AuthenticationForm()
    form.fields['username'].widget.attrs.update({'class': 'form-control'})
    form.fields['password'].widget.attrs.update({'class': 'form-control'})
    return render(request, 'account/account.html', {'form': form})


@require_POST
def login_ajax(request):
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        login(request, form.get_user())
        return JsonResponse({'success': True, 'username': form.get_user().username})
    errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
    return JsonResponse({'success': False, 'errors': errors})


@require_POST
def logout_ajax(request):
    logout(request)
    return JsonResponse({'success': True})
