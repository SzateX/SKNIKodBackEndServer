from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField


class Profile(models.Model):
    # Admin Owner
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    description = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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
    user = models.ForeignKey('Profile', on_delete=models.CASCADE,
                             related_name='profile_links')
    link_type = models.CharField(choices=LINK_TYPES, max_length=100)

    def __str__(self):
        return "%s: %s" % (self.user.user.username, self.link)


class Tag(models.Model):
    # Admin Owner
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"Tag: {self.name}"


class Article(models.Model):
    # Admin Owner
    title = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    text = models.TextField()
    creation_date = models.DateTimeField()
    publication_date = models.DateTimeField(null=True)
    creator = models.ForeignKey('Profile', on_delete=models.CASCADE,
                                related_name='articles')
    authors = models.ManyToManyField('Profile', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    # Admin Owner
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    article = models.ForeignKey('Article', on_delete=models.CASCADE,
                                related_name='comments', null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE,
                                related_name='comments', null=True)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE,
                             related_name='comments')

    def __str__(self):
        return "%s: %s - %s" % (self.article.title, self.user, self.text[0:50] + "..." if len(self.text) > 50 else self.text)


class File(models.Model):
    # Admin
    creation_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE,
                             related_name='files')
    article = models.ForeignKey('Article', on_delete=models.CASCADE,
                                related_name='files')

    def __str__(self):
        return "%s - %s" % (self.user.user.username, self.article.title)


class HardwareRental(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE,
                             related_name='rentals')
    hardware = models.ForeignKey('Hardware', on_delete=models.CASCADE,
                                 related_name='rentals')
    rental_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.user.user.username, self.hardware.name)


class Hardware(models.Model):
    name = models.TextField()
    description = models.TextField()
    serial_number = models.TextField()

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    creation_date = models.DateTimeField()
    publication_date = models.DateTimeField(null=True)
    repository_link = models.CharField(null=True, blank=True, max_length=100)
    creator = models.ForeignKey('Profile', on_delete=models.CASCADE,
                                related_name='projects')
    section = models.ForeignKey('Section', on_delete=models.CASCADE,
                                related_name='projects', null=True)
    authors = models.ManyToManyField('Profile', blank=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    name = models.TextField()
    description = models.TextField()
    isVisible = models.BooleanField()
    icon = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE,
                                related_name='gallery')
    image = ImageField(upload_to='gallery/')

    def __str__(self):
        return "%s - %s" % (self.article.title, self.image.name)

    class Meta:
        verbose_name_plural = "galleries"


class ProjectGallery(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery')
    image = ImageField(upload_to='project_gallery/')