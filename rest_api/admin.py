from django.contrib import admin
from .models import Article, Comment, Tag, File, Section, Gallery, Project, Hardware, Sponsor

# Register your models here.

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(File)
admin.site.register(Section)
admin.site.register(Gallery)
admin.site.register(Project)
admin.site.register(Hardware)
admin.site.register(Sponsor)
