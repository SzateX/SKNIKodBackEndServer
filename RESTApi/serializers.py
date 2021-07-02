from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth.models import User, Group
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import Profile, ProfileLink, Article, Comment, Tag, \
    File, HardwareRental, Hardware, Project, \
    Section, Gallery, RepoLink  # ArticleTag, ArticleAuthor

from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField


class RegisterWithFullNameSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', '')
        }


class UserSerializer(serializers.ModelSerializer):
    is_admin_user = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'profile', 'password',
                  'first_name', 'last_name', 'is_admin_user')
        read_only_fields = ('profile', 'groups')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_is_admin_user(self, obj):
        return obj.is_staff


class ProfileWithoutUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'description', 'profile_links', 'index_number')


class ShortUserSerializer(serializers.ModelSerializer):
    profile = ProfileWithoutUserSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'profile', 'first_name', 'last_name')
        read_only_fields = ('profile', 'groups', 'username')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class ProfileLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLink
        fields = ('id', 'link', 'link_type', 'user')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    profile_links = ProfileLinkSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'description', 'avatar', 'index_number', 'profile_links')


class GallerySerializer(serializers.ModelSerializer):
    thumbnail = HyperlinkedSorlImageField(
        '512x512',
        options={"crop": "center"},
        source='image',
        read_only=True
    )

    class Meta:
        model = Gallery
        fields = ('id', 'image', 'thumbnail')


class ProfileLinkSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLink
        fields = ('id', 'link', 'user', 'link_type')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ArticleSerializer(serializers.ModelSerializer):
    creator = ShortUserSerializer()
    tags = TagSerializer(many=True)
    comments_number = serializers.SerializerMethodField()
    gallery = GallerySerializer(many=True)
    authors = ShortUserSerializer(many=True)

    class Meta:
        model = Article
        fields = (
            'id', 'alias', 'title', 'text', 'creation_date',
            'publication_date', 'creator', 'authors', 'tags', 'comments_number',
            'gallery')

    def get_comments_number(self, obj):
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()
    article = ArticleSerializer()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'creation_date', 'article', 'parent', 'user', 'children')
        depth = 2
    
    def get_children(self, obj):
        child = Comment.objects.filter(parent=obj).order_by('-creation_date')
        serializer = CommentSerializer(instance=child, many=True)
        return serializer.data


class CommentSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'creation_date', 'article', 'parent', 'user')

    def validate(self, data):
        if ('article_id' in data or 'project_id' in data) and not ('article_id' in data and 'project_id' in data):
            raise serializers.ValidationError("U have to provide article id or project id")
        super(CommentSaveSerializer, self).validate(data)


class ArticleSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = (
            'id', 'alias', 'title', 'text', 'creation_date', 'publication_date',
            'creator', 'tags', 'authors', 'gallery')


class FileSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    article = ArticleSerializer()

    class Meta:
        model = File
        fields = ('id', 'creation_date', 'user', 'article')


class FileSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'creation_date', 'user', 'article')


class HardwareSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hardware
        fields = ('id', 'name', 'description', 'serial_number', 'status')


class HardwareSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hardware
        fields = ('id', 'name', 'description', 'serial_number')


class HardwareRentalSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()
    hardware = HardwareSerializer()

    class Meta:
        model = HardwareRental
        fields = ('id', 'rental_date', 'return_date', 'user', 'hardware', 'file')


class HardwareRentalSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareRental
        fields = ('id', 'rental_date', 'return_date', 'user', 'hardware')


class SectionSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(many=True)

    class Meta:
        model = Section
        fields = ('id', 'name', 'description', 'isVisible', 'icon', 'gallery')


class SectionSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'name', 'description', 'isVisible', 'icon', 'gallery')


class RepoLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepoLink
        fields = ('id', 'link', 'link_type', 'project')


class ProjectSerializer(serializers.ModelSerializer):
    creator = ShortUserSerializer()
    section = SectionSerializer()
    authors = ShortUserSerializer(many=True)
    repository_links = RepoLinkSerializer(many=True)
    gallery = GallerySerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'text', 'creation_date', 'publication_date',
                  'repository_links', 'creator', 'section', 'authors', 'gallery')


class ProjectSaveSerializer(serializers.ModelSerializer):
    repository_links = serializers.PrimaryKeyRelatedField(many=True, required=True, queryset=RepoLink.objects.all())
    authors = serializers.PrimaryKeyRelatedField(many=True, required=True, queryset=User.objects.all())

    class Meta:
        model = Project
        fields = ('id', 'title', 'text', 'creation_date', 'publication_date',
                  'repository_links', 'creator', 'section', 'authors', 'gallery')
        extra_kwargs = {'gallery': {'required': False}}
