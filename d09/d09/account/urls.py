from django.urls import path
from . import views

urlpatterns = [
    path('', views.account, name='account'),
    path('login/', views.login_ajax, name='login_ajax'),
    path('logout/', views.logout_ajax, name='logout_ajax'),
]
