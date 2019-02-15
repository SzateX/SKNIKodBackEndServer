from django.contrib.auth.models import User, Group
from rest_framework import viewsets

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


class HardwareRentalSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = HardwareRental.objects.all()
    serializer_class = HardwareRentalSerializer


class HardwareSet(viewsets.ModelViewSet):
    permission_classes =  (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerializer


class ProjectSet(viewsets.ModelViewSet):
    permission_classes =  (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectAuthorSet(viewsets.ModelViewSet):
    permission_classes =  (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = ProjectAuthor.objects.all()
    serializer_class = ProjectAuthorSerializer

class SectionSet(viewsets.ModelViewSet):
    permission_classes =  (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Section.objects.all()
    serializer_class = SectionSerializer