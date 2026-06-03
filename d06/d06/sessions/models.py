from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    @property
    def reputation(self):
        total = 0
        for tip in self.tip_set.prefetch_related('upvotes', 'downvotes'):
            total += tip.upvotes.count() * 5
            total -= tip.downvotes.count() * 2
        return total

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        if perm == 'ex_sessions.can_downvote' and self.reputation >= 15:
            return True
        if perm == 'ex_sessions.delete_tip' and self.reputation >= 30:
            return True
        return super().has_perm(perm, obj)


class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='upvoted_tips', blank=True
    )
    downvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='downvoted_tips', blank=True
    )

    class Meta:
        permissions = [
            ('can_downvote', 'Can downvote tips'),
        ]
