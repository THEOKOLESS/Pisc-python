from django.views.generic import ListView, DetailView, RedirectView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from .models import Article, UserFavoriteArticle


class HomeView(RedirectView):
    pattern_name = 'articles'


class ArticleListView(ListView):
    model = Article
    template_name = 'advanced/articles.html'
    context_object_name = 'articles'
    ordering = ['-created']


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'advanced/detail.html'
    context_object_name = 'article'


class PublicationsView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'advanced/publications.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class FavouritesView(LoginRequiredMixin, ListView):
    model = UserFavoriteArticle
    template_name = 'advanced/favourites.html'
    context_object_name = 'favourites'

    def get_queryset(self):
        return UserFavoriteArticle.objects.filter(user=self.request.user)


class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'advanced/register.html'
    success_url = reverse_lazy('login')


class PublishView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'synopsis', 'content']
    template_name = 'advanced/publish.html'
    success_url = reverse_lazy('publications')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AddToFavouriteView(LoginRequiredMixin, CreateView):
    model = UserFavoriteArticle
    fields = []

    #avoid error when user tries to access this view with GET method, redirect to article detail page
    def get(self, _request, *_args, **_kwargs):
        return redirect(reverse('detail', kwargs={'pk': self.kwargs['pk']}))

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.article_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.kwargs['pk']})
