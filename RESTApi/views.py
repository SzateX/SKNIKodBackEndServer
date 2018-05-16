from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .models import Profile, RepoLink, Article, Comment, Tag, ArticleAuthor, \
    ArticleTag, File
from RESTApi.serializers import UserSerializer, GroupSerializer, \
    ProfileSerializer, RepoLinkSerializer, ArticleSerializer, \
    CommentSerializer, TagSerializer, ArticleAuthorSerializer, \
    ArticleTagSerializer, FileSerializer

from rest_framework import permissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


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


class RepoLinkViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = RepoLink.objects.all()
    serializer_class = RepoLinkSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Article.objects.all().order_by('-publication_date')
    serializer_class = ArticleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Comment.objects.all().order_by('-creation_date')
    serializer_class = CommentSerializer


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleAuthorSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = ArticleAuthor.objects.all()
    serializer_class = ArticleAuthorSerializer


class ArticleTagSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = ArticleTag.objects.all()
    serializer_class = ArticleTagSerializer


class FileSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = File.objects.all()
    serializer_class = FileSerializer
