from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    # Admin Owner
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    technologies = models.TextField(null=True)
    interests = models.TextField(null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class RepoLink(models.Model):
    # Admin Owner
    link = models.CharField(max_length=100)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)


class Article(models.Model):
    # Admin Owner
    title = models.CharField(max_length=100)
    text = models.TextField()
    creation_date = models.DateTimeField()
    publication_date = models.DateTimeField(null=True)
    article_type = models.ForeignKey('ArticleType', on_delete=models.CASCADE)
    repository_link = models.CharField(null=True, max_length=100)
    creator = models.ForeignKey('Profile', on_delete=models.CASCADE)


class Comment(models.Model):
    # Admin Owner
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)


class Tag(models.Model):
    # Admin Owner
    name = models.CharField(max_length=50)


class ArticleAuthor(models.Model):
    # Admin
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)


class ArticleTag(models.Model):
    # Admin
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)


class File(models.Model):
    # Admin
    creation_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)


class ArticleType(models.Model):
    name = models.TextField()


class HardwareRental(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    hardware_piece = models.ForeignKey('HardwarePiece', on_delete=models.CASCADE)
    rental_date = models.DateTimeField()
    return_date = models.DateTimeField()


class HardwarePiece(models.Model):
    hardware = models.ForeignKey('Hardware', on_delete=models.CASCADE)


class Hardware(models.Model):
    name = models.TextField()
    description = models.TextField()
