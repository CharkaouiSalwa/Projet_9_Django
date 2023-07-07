from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User




class Ticket(models.Model):
    title = models.fields.CharField(max_length=128)
    description = models.fields.TextField(max_length=2048,blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='chemin/images/', blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('update_ticket', args=[str(self.id)])


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        'Note',
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField('Titre', max_length=128)
    body = models.CharField('commentaire', max_length=8192, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user', )

    def __str__(self):
        return self.followed_user.username