from django.contrib import admin
from django.conf.urls import include
from django.urls import re_path
from django.conf.urls.static import static
from rest_framework import routers

from dynamic_preferences.api.viewsets import GlobalPreferencesViewSet

from rest_api.views import ArticleViewSetList, ArticleViewSetDetail, CommentViewSetList, CommentViewSetDetail, \
    TagViewSetList, TagViewSetDetail, FileViewSetList, FileViewSetDetail, GalleryViewSetList, GalleryViewSetDetail, \
    HardwareViewSetList, HardwareViewSetDetail, SectionViewSetList, SectionViewSetDetail, ProjectViewSetList, \
    ProjectViewSetDetail, SponsorViewSetList, SponsorViewSetDetail, GenericLinkViewSetList, GenericLinkViewSetDetail, \
    FooterLinkListView, FooterLinkDetailView

from user.views import ProfileViewSetDetail, ProfileViewSetList
from . import settings
from rest_framework_swagger.views import get_swagger_view

router = routers.DefaultRouter()

router.register(r'global', GlobalPreferencesViewSet)
api_patterns = [
    re_path(r'^preferences/', include(router.urls))
]

schema_view = get_swagger_view(title='SKNI KOD Website API')

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include(api_patterns)),
    re_path(r'^api/articles/$', ArticleViewSetList.as_view(), name='article_list'),
    re_path(r'^api/articles/(?P<pk>\d+)/$', ArticleViewSetDetail.as_view(), name='article_list'),
    re_path(r'^api/comments/$', CommentViewSetList.as_view(), name='comment_list'),
    re_path(r'^api/comments/(?P<pk>\d+)/$', CommentViewSetDetail.as_view(), name='comment_detail'),
    re_path(r'^api/tags/$', TagViewSetList.as_view(), name='tag_list'),
    re_path(r'^api/tags/(?P<pk>\d+)/$', TagViewSetDetail.as_view(), name='tag_detail'),
    re_path(r'^api/files/$', FileViewSetList.as_view(), name='file_list'),
    re_path(r'^api/files/(?P<pk>\d+)/$', FileViewSetDetail.as_view(), name='file_detail'),
    re_path(r'^api/gallery/$', GalleryViewSetList.as_view(), name='gallery_detail'),
    re_path(r'^api/gallery/(?P<pk>\d+)/$', GalleryViewSetDetail.as_view(), name='gallery_detail'),
    re_path(r'^api/hardwares/$', HardwareViewSetList.as_view(), name='hardware_list'),
    re_path(r'^api/hardwares/(?P<pk>\d+)/$', HardwareViewSetDetail.as_view(), name='hardware_detail'),
    re_path(r'^api/section/$', SectionViewSetList.as_view(), name='section_list'),
    re_path(r'^api/section/(?P<pk>\d+)/$', SectionViewSetDetail.as_view(), name='section_detail'),
    re_path(r'^api/projects/$', ProjectViewSetList.as_view(), name='project_detail'),
    re_path(r'^api/projects/(?P<pk>\d+)/$', ProjectViewSetDetail.as_view(), name='project_detail'),
    re_path(r'^api/profiles/$', ProfileViewSetList.as_view(), name='profiles_detail'),
    re_path(r'^api/profiles/(?P<pk>\d+)/$', ProfileViewSetDetail.as_view(), name='profiles_detail'),
    re_path(r'^api/sponsors/$', SponsorViewSetList.as_view(), name='sponsor_list'),
    re_path(r'^api/sponsors/(?P<pk>\d+)/$', SponsorViewSetDetail.as_view(), name='sponsor_detail'),
    re_path(r'^api/generic_links/$', GenericLinkViewSetList.as_view(), name='generic_link_detail'),
    re_path(r'^api/generic_links/(?P<pk>\d+)/$', GenericLinkViewSetDetail.as_view(), name='generic_link_list'),
    re_path(r'^api/footer_links/$', FooterLinkListView.as_view(), name='footer_link_detail'),
    re_path(r'^api/footer_links/(?P<pk>\d+)/$', FooterLinkDetailView.as_view(), name='footer_link_list'),
    re_path(r'^docs$', schema_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)