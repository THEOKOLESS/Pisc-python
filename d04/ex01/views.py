from django.shortcuts import render

# Create your views here.

def django(request):
    return render(request, 'ex01/django.html')

def affichage(request):
    return render(request, 'ex01/affichage.html')

def templates(request):
    return render(request, 'ex01/templates.html')