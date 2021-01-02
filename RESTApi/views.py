import django_filters
from django.contrib.auth.models import User, Group
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from RESTApi.serializers import *

from rest_framework import permissions

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView, SocialConnectView


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = 'http://127.0.0.1:8000/accounts/github/login/callback/'
    client_class = OAuth2Client


class GitHubConnect(SocialConnectView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = 'http://127.0.0.1:8000/accounts/github/login/callback/'
    client_class = OAuth2Client


class IndexTemplateView(TemplateView):
    template_name = 'index.html'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = UserUpdateSerializer

        return serializer_class


class UserViewSetDetail(APIView):
    queryset = User.objects.none()

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = UserSerializer(queryset)
        return Response(serializer.data)
        
    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = UserUpdateSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request,  pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = UserUpdateSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSetList(APIView):
    queryset = User.objects.none()
    
    def get(self, format=None):
        queryset = User.objects.all().order_by('-date_joined')
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class ProfileLinkViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = ProfileLink.objects.all()
    serializer_class = ProfileLinkSerializer

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return ProfileLinkSaveSerializer

        return self.serializer_class


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Article.objects.all().order_by('-publication_date')
    serializer_class = ArticleSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        tag_id = self.request.query_params.get('tag', None)
        tag_name = self.request.query_params.get('tagname', None)
        author_id = self.request.query_params.get('author', None)
        author_name = self.request.query_params.get('authorname', None)
        if tag_id is not None:
            return Article.objects.filter(tags=tag_id).order_by(
                '-publication_date')
        if tag_name is not None:
            return Article.objects.filter(tags__name=tag_name).order_by(
                '-publication_date')
        if author_id is not None:
            return Article.objects.filter(authors=author_id).order_by('-publication_date')
        if author_name is not None:
            return Article.objects.filter(authors__user__username=author_name).order_by('-publication_date')
        return Article.objects.all().order_by('-publication_date')

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
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
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


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


class SectionSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class GallerySet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

    def get_queryset(self):
        article_id = self.request.query_params.get('article', None)
        if article_id is None:
            return Gallery.objects.all()
        return Gallery.objects.filter(article=article_id)
