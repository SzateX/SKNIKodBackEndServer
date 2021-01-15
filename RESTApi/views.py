import django_filters
from django.contrib.auth.models import User, Group
from django.http import Http404
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
            serializer.save()
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


class GroupViewSetDetail(APIView):
    queryset = User.objects.none()

    def get_object(self, pk=None):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GroupSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GroupSerializer(queryset, data=request.data)
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
        serializer = GroupSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupViewSetList(APIView):
    queryset = User.objects.none()

    def get(self, format=None):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSetDetail(APIView):
    queryset = Profile.objects.none()

    def get_object(self, pk=None):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk=pk)
        serializer = ProfileSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ProfileSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ProfileSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSetList(APIView):
    queryset = Profile.objects.none()
    pagination_class = LimitOffsetPagination

    def get(self, request, format=None):
        queryset = Profile.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        if result_page is not None:
            serializer = ProfileSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileLinkViewSetDetail(APIView):
    queryset = ProfileLink.objects.none()

    def get_object(self, pk=None):
        try:
            return ProfileLink.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk=pk)
        serializer = ProfileLinkSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ProfileLinkSaveSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ProfileLinkSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileLinkViewSetList(APIView):
    queryset = ProfileLink.objects.none()
    pagination_class = LimitOffsetPagination

    def get(self, request, format=None):
        queryset = ProfileLink.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        if result_page is not None:
            serializer = ProfileLinkSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = ProfileLinkSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProfileLinkSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      
class ArticleViewSetDetail(APIView):
    queryset = Article.objects.none()

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ArticleSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ArticleSaveSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ArticleSaveSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleViewSetList(APIView):
    queryset = Article.objects.none()
    pagination_class = LimitOffsetPagination

    def get_objects(self):
        tag_id = self.request.query_params.get('tag', None)
        tag_name = self.request.query_params.get('tagname', None)
        author_id = self.request.query_params.get('author', None)
        author_name = self.request.query_params.get('authorname', None)
        if tag_id is not None:
            return Article.objects.filter(tags=tag_id).order_by('-publication_date')
        if tag_name is not None:
            return Article.objects.filter(tags__name=tag_name).order_by('-publication_date')
        if author_id is not None:
            return Article.objects.filter(authors=author_id).order_by('-publication_date')
        if author_name is not None:
            return Article.objects.filter(authors__user__username=author_name).order_by('-publication_date')
        return Article.objects.all().order_by('-publication_date')

    def get(self, request, format=None):
        queryset = self.get_objects()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        if result_page is not None:
            serializer = ArticleSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ArticleSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSetDetail(APIView):
    queryset = Comment.objects.none()

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = CommentSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = CommentSaveSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = CommentSaveSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSetList(APIView):
    queryset = Comment.objects.none()

    def get_objects(self):
        article_id = self.request.query_params.get('article', None)
        if article_id is None:
            return Comment.objects.all().order_by('-creation_date')
        return Comment.objects.filter(article=article_id).order_by('-creation_date')

    def get(self, request, format=None):
        queryset = self.get_objects()
        serializer = CommentSerializer(queryset, many="True")
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = CommentSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class ProjectSetDetail(APIView):
    queryset = Comment.objects.none()

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ProjectSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ProjectSaveSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ProjectSaveSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectSetList(APIView):
    queryset = User.objects.none()
    pagination_class = LimitOffsetPagination
    
    def get(self, request, format=None):
        queryset = Project.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        if result_page is not None:
            serializer = ProjectSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ProjectSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
