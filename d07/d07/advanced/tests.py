from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import translation
from .models import Article, UserFavoriteArticle


class SetUpMixin:
    def setUp(self):
        translation.activate('en')
        self.user = User.objects.create_user('testuser', password='pass')
        self.article = Article.objects.create(
            title='Test Article',
            author=self.user,
            synopsis='Test synopsis',
            content='Test content',
        )


class FavouritesViewOnlyAccessibleToLoggedInUserTest(SetUpMixin, TestCase):

    def test_favourites_view_redirects_unauthenticated_user_to_login(self):
        response = self.client.get(reverse('favourites'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_favourites_template_not_rendered_for_unauthenticated_user(self):
        response = self.client.get(reverse('favourites'))
        self.assertTemplateNotUsed(response, 'advanced/favourites.html')

    def test_favourites_view_accessible_to_logged_in_user(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('favourites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'advanced/favourites.html')


class PublicationsViewOnlyAccessibleToLoggedInUserTest(SetUpMixin, TestCase):

    def test_publications_view_redirects_unauthenticated_user_to_login(self):
        response = self.client.get(reverse('publications'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_publications_template_not_rendered_for_unauthenticated_user(self):
        response = self.client.get(reverse('publications'))
        self.assertTemplateNotUsed(response, 'advanced/publications.html')

    def test_publications_view_accessible_to_logged_in_user(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('publications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'advanced/publications.html')


class PublishViewOnlyAccessibleToLoggedInUserTest(SetUpMixin, TestCase):

    def test_publish_view_redirects_unauthenticated_user_to_login(self):
        response = self.client.get(reverse('publish'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_publish_template_not_rendered_for_unauthenticated_user(self):
        response = self.client.get(reverse('publish'))
        self.assertTemplateNotUsed(response, 'advanced/publish.html')

    def test_publish_view_accessible_to_logged_in_user(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('publish'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'advanced/publish.html')


class RegisterFormNotAccessibleToLoggedInUserTest(SetUpMixin, TestCase):

    def test_register_view_redirects_logged_in_user(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)

    def test_register_template_not_rendered_for_logged_in_user(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('register'))
        self.assertTemplateNotUsed(response, 'advanced/register.html')


class UserCannotAddSameArticleToFavouritesTwiceTest(SetUpMixin, TestCase):

    def test_adding_same_article_to_favourites_twice_creates_only_one_entry(self):
        self.client.login(username='testuser', password='pass')
        self.client.post(reverse('add_favourite', kwargs={'pk': self.article.pk}))
        self.client.post(reverse('add_favourite', kwargs={'pk': self.article.pk}))
        count = UserFavoriteArticle.objects.filter(user=self.user, article=self.article).count()
        self.assertEqual(count, 1)
