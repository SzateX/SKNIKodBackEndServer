from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .models import SiteUser, RepoLink, Article, Comment, Tag, ArticleAuthor, \
    ArticleTag, File
from RESTApi.serializers import UserSerializer, GroupSerializer, \
    SiteUserSerializer, RepoLinkSerializer, ArticleSerializer, \
    CommentSerializer, TagSerializer, ArticleAuthorSerializer, \
    ArticleTagSerializer, FileSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class SiteUserViewSet(viewsets.ModelViewSet):
    queryset = SiteUser.objects.all()
    serializer_class = SiteUserSerializer


class RepoLinkViewSet(viewsets.ModelViewSet):
    queryset = RepoLink.objects.all()
    serializer_class = RepoLinkSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-publication_date')
    serializer_class = ArticleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-creation_date')
    serializer_class = CommentSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleAuthorSet(viewsets.ModelViewSet):
    queryset = ArticleAuthor.objects.all()
    serializer_class = ArticleAuthor


class ArticleTagSet(viewsets.ModelViewSet):
    queryset = ArticleTag.objects.all()
    serializer_class = ArticleTagSerializer


class FileSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
