from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from rest_api.models import GenericLink


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    description = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True)
    index_number = models.CharField(max_length=6, default=None, null=True)
    links = GenericRelation(GenericLink)

    def __str__(self):
        return self.user.username
