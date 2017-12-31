from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(SiteUser)
admin.site.register(RepoLink)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(ArticleAuthor)
admin.site.register(ArticleTag)
admin.site.register(File)
