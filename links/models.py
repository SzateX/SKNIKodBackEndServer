from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from user.models import Profile


class GenericLink(models.Model):
    # Admin Owner
    GITHUB = 'GITHUB'
    GITLAB = 'GITLAB'
    BITBUCKET = 'BITBUCKET'
    BLOG = 'BLOG'
    PORTFOLIO = 'PORTFOLIO'
    OTHER = 'OTHER'
    LINK_TYPES = [
        (GITHUB, 'GITHUB'),
        (GITLAB, 'GITLAB'),
        (BITBUCKET, 'BITBUCKET'),
        (BLOG, 'BLOG'),
        (PORTFOLIO, 'PORTFOLIO'),
        (OTHER, 'OTHER')
    ]

    link = models.URLField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    linked_object = GenericForeignKey('content_type', 'object_id')
    link_type = models.CharField(choices=LINK_TYPES, max_length=100)

    def __str__(self):
        return "%s" % self.link


class ProfileLink(models.Model):
    # Admin Owner
    GITHUB = 'GITHUB'
    GITLAB = 'GITLAB'
    BITBUCKET = 'BITBUCKET'
    BLOG = 'BLOG'
    PORTFOLIO = 'PORTFOLIO'
    OTHER = 'OTHER'
    LINK_TYPES = [
        (GITHUB, 'GITHUB'),
        (GITLAB, 'GITLAB'),
        (BITBUCKET, 'BITBUCKET'),
        (BLOG, 'BLOG'),
        (PORTFOLIO, 'PORTFOLIO'),
        (OTHER, 'OTHER')
    ]

    link = models.URLField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,
                             related_name='profile_links')
    link_type = models.CharField(choices=LINK_TYPES, max_length=100)

    def __str__(self):
        return "%s: %s" % (self.user.user.username, self.link)