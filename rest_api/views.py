from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions

from rest_api.models import Article, Comment, Tag, File, HardwareRental, Hardware, Project, Section, Gallery, Sponsor, \
    FooterLink
from rest_api.serializers import ArticleSerializer, ArticleSaveSerializer, CommentSerializer, CommentSaveSerializer, \
    TagSerializer, FileSerializer, FileSaveSerializer, HardwareRentalSerializer, HardwareRentalSaveSerializer, \
    HardwareSerializer, HardwareSaveSerializer, ProjectSerializer, ProjectSaveSerializer, SectionSaveSerializer, \
    SectionSerializer, GallerySerializer, SponsorSerializer, FooterLinkSerializer
from user.models import Profile
from utils.custom_permissions import IsOwnerOrAdminForCommentViewOrReadOnly


class ArticleViewSetDetail(APIView):
    queryset = Article.objects.none()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleViewSetList(APIView):
    queryset = Article.objects.none()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    pagination_class = LimitOffsetPagination

    def get_objects(self):
        tag_id = self.request.query_params.get('tag', None)
        tag_name = self.request.query_params.get('tagname', None)
        author_id = self.request.query_params.get('author', None)
        author_name = self.request.query_params.get('authorname', None)
        group = self.request.query_params.get('group', None)
        if tag_id is not None:
            return Article.objects.filter(tags=tag_id).order_by('-publication_date')
        if tag_name is not None:
            return Article.objects.filter(tags__name=tag_name).order_by('-publication_date')
        if author_id is not None:
            return Article.objects.filter(authors=author_id).order_by('-publication_date')
        if author_name is not None:
            return Article.objects.filter(authors__user__username=author_name).order_by('-publication_date')
        if group is not None:
            return Article.objects.filter(group=group).order_by('-publication_date')
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
    permission_classes = [IsOwnerOrAdminForCommentViewOrReadOnly]

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
        self.check_object_permissions(self.request, queryset)
        serializer = CommentSaveSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        self.check_object_permissions(self.request, queryset)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        self.check_object_permissions(self.request, queryset)
        serializer = CommentSaveSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSetList(APIView):
    queryset = Comment.objects.none()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_objects(self):
        article_id = self.request.query_params.get('article', None)
        if article_id is not None:
            return Comment.objects.filter(article=article_id).order_by('-creation_date')
        else: return Comment.objects.all().order_by('-creation_date')

    def get(self, request, format=None):
        queryset = self.get_objects()
        serializer = CommentSerializer(queryset, many="True")
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagViewSetDetail(APIView):
    queryset = Tag.objects.none()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_object(self, pk):
        try:
            return Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TagSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TagSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request,  pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TagSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagViewSetList(APIView):
    queryset = Tag.objects.none()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get(self, format=None):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileViewSetDetail(APIView):
    queryset = File.objects.none()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = FileSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = FileSaveSerializer(queryset, data=request.data)
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
        serializer = FileSaveSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileViewSetList(APIView):
    queryset = File.objects.none()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    
    def get(self, format=None):
        queryset = File.objects.all()
        serializer = FileSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FileSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HardwareRentalSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = HardwareRental.objects.all()
    serializer_class = HardwareRentalSerializer

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return HardwareRentalSaveSerializer
        return self.serializer_class


class HardwareRentalViewSetDetail(APIView):
    queryset = HardwareRental.objects.none()
    permission_classes = (permissions.DjangoModelPermissions,)

    def get_object(self, pk=None):
        try:
            return HardwareRental.objects.get(pk=pk)
        except HardwareRental.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk=pk)
        serializer = HardwareRentalSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = HardwareRentalSaveSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = HardwareRentalSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HardwareSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerializer
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return HardwareSaveSerializer
        return self.serializer_class


class HardwareViewSetDetail(APIView):
    queryset = Hardware.objects.none()
    permission_classes = (permissions.DjangoModelPermissions,)

    def get_object(self, pk=None):
        try:
            return Hardware.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk=pk)
        serializer = HardwareSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = HardwareSaveSerializer(queryset, data=request.data)
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
        serializer = HardwareSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HardwareViewSetList(APIView):
    queryset = Hardware.objects.none()
    permission_classes = (permissions.DjangoModelPermissions,)
    pagination_class = LimitOffsetPagination

    def get(self, request, format=None):
        queryset = Hardware.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        if result_page is not None:
            serializer = HardwareSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = HardwareSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HardwareSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSetDetail(APIView):
    queryset = Project.objects.none()
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSetList(APIView):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Project.objects.none()
    pagination_class = LimitOffsetPagination

    def get(self, request, format=None):
        queryset = Project.objects.all().order_by('-id')
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


class SectionViewSetDetail(APIView):
    queryset = Section.objects.none()
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def get_object(self, pk=None):
        try:
            return Section.objects.get(pk=pk)
        except Section.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk=pk)
        serializer = SectionSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = SectionSaveSerializer(queryset, data=request.data)
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
        serializer = SectionSaveSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SectionViewSetList(APIView):
    queryset = Section.objects.none()
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def get(self, format=None):
        queryset = Section.objects.all()
        serializer = SectionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SectionSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryViewSetDetail(APIView):
    queryset = Gallery.objects.none()
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def get_object(self, pk):
        try:
            return Gallery.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GallerySerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GallerySerializer(queryset, data=request.data)
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
        serializer = GallerySerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryViewSetList(APIView):
    queryset = Gallery.objects.none()
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def get_objects(self):
        article_id = self.request.query_params.get('article', None)
        if article_id is None:
            return Gallery.objects.all()
        return Gallery.objects.filter(article=article_id)

    def get(self, request, format=None):
        queryset = self.get_objects()
        serializer = GallerySerializer(queryset, many="True")
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SponsorViewSetDetail(APIView):
    queryset = Sponsor.objects.none()
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def get_object(self, pk):
        try:
            return Sponsor.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = SponsorSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = SponsorSerializer(queryset, data=request.data)
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
        serializer = SponsorSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SponsorViewSetList(APIView):
    queryset = Sponsor.objects.none()
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def get(self, format=None):
        queryset = Sponsor.objects.all()
        serializer = SponsorSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SponsorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FooterLinkListView(APIView):
    queryset = FooterLink.objects.none()
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def get(self, request, format=None):
        queryset = FooterLink.objects.all()
        serializer = FooterLinkSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FooterLinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class FooterLinkDetailView(APIView):
    queryset = FooterLink.objects.none()
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def get_object(self, pk=None):
        try:
            return FooterLink.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk=pk)
        serializer = FooterLinkSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = FooterLinkSerializer(queryset, data=request.data)
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
        serializer = FooterLinkSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)