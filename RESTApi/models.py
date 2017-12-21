from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class SiteUser(User):
    technologies = models.TextField(null=True)
    interests = models.TextField(null=True)


class RepoLink(models.Model):
    link = models.CharField(max_length=100)
    user = models.ForeignKey('SiteUser', on_delete=models.CASCADE)


class Article(models.Model):
    ArticleTypes = (
        (1, 'Project'),
        (2, 'Article'),
    )

    title = models.CharField(max_length=100)
    text = models.TextField()
    creation_date = models.DateTimeField()
    publication_date = models.DateTimeField(null=True)
    article_type = models.IntegerField(choices=ArticleTypes)
    repository_link = models.CharField(null=True, max_length=100)
    creator = models.ForeignKey('SiteUser', on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    user = models.ForeignKey('SiteUser', on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=50)


class ArticleAuthor(models.Model):
    user = models.ForeignKey('SiteUser', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)


class ArticleTag(models.Model):
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)


class File(models.Model):
    creation_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey('SiteUser', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
