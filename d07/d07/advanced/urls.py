from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('articles/<int:pk>/favourite/', views.AddToFavouriteView.as_view(), name='add_favourite'),
    path('publications/', views.PublicationsView.as_view(), name='publications'),
    path('publish/', views.PublishView.as_view(), name='publish'),
    path('favourites/', views.FavouritesView.as_view(), name='favourites'),
    path('login/', LoginView.as_view(template_name='advanced/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
