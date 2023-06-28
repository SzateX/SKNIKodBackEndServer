from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from user.models import Profile


class Tag(models.Model):
    # Admin Owner
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"Tag: {self.name}"


class Gallery(models.Model):

    gallery_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="gallery/")
    thumbnail_visibility = models.BooleanField(default=False)
    text_visibility = models.BooleanField(default=False)
    gallery_visibility = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.gallery_name, self.image.name)

    class Meta:
        verbose_name_plural = "galleries"


class Article(models.Model):
    # Admin Owner
    title = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    text = models.TextField()
    group = models.CharField(max_length=10, choices=(('News', 'News'), ('Article', 'Article')))
    creation_date = models.DateTimeField()
    publication_date = models.DateTimeField(null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='articles')
    authors = models.ManyToManyField(User, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    gallery = models.ManyToManyField('Gallery', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    # Admin Owner
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    article = models.ForeignKey('Article', on_delete=models.CASCADE,
                                related_name='comments', null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                                related_name='comments', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='comments')

    def save(self, *args, **kwargs):
        if (self.article or self.parent) and not (self.article and self.parent):
            pass
        else:
            raise Exception("U have to provide article id or parent id")
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return "%s: %s - %s" % (self.article.title, self.user, self.text[0:50] + "..." if len(self.text) > 50 else self.text)


class File(models.Model):
    # Admin
    creation_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,
                             related_name='files')
    article = models.ForeignKey('Article', on_delete=models.CASCADE,
                                related_name='files')

    def __str__(self):
        return "%s - %s" % (self.user.user.username, self.article.title)


class HardwareRental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='rentals')
    hardware = models.ForeignKey('Hardware', on_delete=models.CASCADE,
                                 related_name='rentals')
    rental_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    file = models.FileField(upload_to='hardware_rental/', blank=True)

    def __str__(self):
        return "%s - %s" % (self.user.username, self.hardware.name)


class Hardware(models.Model):
    statusy = (('Rented', 'Rented'),
               ('Available', 'Available'),
               ('Unavailable', 'Unavailable'))
    name = models.TextField()
    description = models.TextField()
    serial_number = models.TextField()
    status = models.TextField(choices=statusy, default='Unavailable')

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    creation_date = models.DateTimeField()
    publication_date = models.DateTimeField(null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='projects')
    section = models.ForeignKey('Section', on_delete=models.CASCADE,
                                related_name='projects', null=True)
    authors = models.ManyToManyField(User, blank=True)

    gallery = models.ManyToManyField('Gallery', blank=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    name = models.TextField()
    description = models.TextField()
    isVisible = models.BooleanField()
    icon = models.TextField(null=True, blank=True)
    gallery = models.ManyToManyField('Gallery', blank=True)

    def __str__(self):
        return self.name


class Sponsor(models.Model):
    name = models.CharField(max_length=60)
    url = models.URLField(null=True)
    logo = models.ImageField(upload_to='sponsor_logo/')


class FooterLink(models.Model):
    link = models.URLField()
    title = models.CharField(max_length=128)
    icon = models.CharField(max_length=64)
    color = models.CharField(max_length=64)

    def __str__(self):
        return self.title