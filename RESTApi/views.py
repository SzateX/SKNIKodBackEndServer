import django_filters
from django.contrib.auth.models import User, Group
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import *
from RESTApi.serializers import *

from rest_framework import permissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = UserUpdateSerializer

        return serializer_class


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = LimitOffsetPagination


class RepoLinkViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = RepoLink.objects.all()
    serializer_class = RepoLinkSerializer

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return RepoLinkSaveSerializer

        return self.serializer_class


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Article.objects.all().order_by('-publication_date')
    serializer_class = ArticleSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        tag_id = self.request.query_params.get('tag', None)
        tag_name = self.request.query_params.get('tagname', None)
        if tag_id is not None:
            return Article.objects.filter(tags__tag=tag_id).order_by(
                '-publication_date')
        if tag_name is not None:
            return Article.objects.filter(tags__tag__name=tag_name).order_by('-publication_date')
        return Article.objects.all().order_by('-publication_date')

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return ArticleSaveSerializer
        return self.serializer_class


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Comment.objects.all().order_by('-creation_date')
    serializer_class = CommentSerializer

    def get_queryset(self):
        article_id = self.request.query_params.get('article', None)
        if article_id is None:
            return Comment.objects.all()
        return Comment.objects.filter(article=article_id)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return CommentSaveSerializer
        return self.serializer_class


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleAuthorSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = ArticleAuthor.objects.all()
    serializer_class = ArticleAuthorSerializer

    def get_serializer_class(self):
        if self.request.methos in ('POST', 'PUT'):
            return ArticleAuthorSaveSerializer
        return self.serializer_class


class ArticleTagSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = ArticleTag.objects.all()
    serializer_class = ArticleTagSerializer

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return ArticleTagSaveSerializer
        return self.serializer_class


class FileSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return FileSaveSerializer
        return self.serializer_class


class HardwareRentalSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = HardwareRental.objects.all()
    serializer_class = HardwareRentalSerializer

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return HardwareRentalSaveSerializer
        return self.serializer_class


class HardwareSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerializer
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return HardwareSaveSerializer
        return self.serializer_class


class ProjectSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return ProjectSaveSerializer
        return self.serializer_class


class ProjectAuthorSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = ProjectAuthor.objects.all()
    serializer_class = ProjectAuthorSerializer

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return ProjectAuthorSaveSerializer
        return self.serializer_class


class SectionSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

