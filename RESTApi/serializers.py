from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth.models import User, Group
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import Profile, ProfileLink, Article, Comment, Tag, \
    File, HardwareRental, Hardware, Project, \
    Section, Gallery  # ArticleTag, ArticleAuthor

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
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'profile', 'password',
                  'first_name', 'last_name')
        read_only_fields = ('profile', 'groups')
        extra_kwargs = {
            'password': {'write_only': True}
        }

        depth = 1

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


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'profile', 'first_name', 'last_name')
        read_only_fields = ('profile', 'groups', 'username')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'description', 'avatar', 'profile_links')


class GallerySerializer(serializers.ModelSerializer):
    thumbnail = HyperlinkedSorlImageField(
        '512x512',
        options={"crop": "center"},
        source='image',
        read_only=True
    )

    class Meta:
        model = Gallery
        fields = ('id', 'article', 'image', 'thumbnail')


class ProfileLinkSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = ProfileLink
        fields = ('id', 'link', 'user', 'link_type')


class ProfileLinkSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLink
        fields = ('id', 'link', 'user', 'link_type')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class CommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'creation_date', 'article_id', 'user')
        depth = 2


class CommentSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'creation_date', 'article_id', 'user')
        depth = 2


class ArticleSerializer(serializers.ModelSerializer):
    creator = ProfileSerializer()
    tags = TagSerializer(many=True)
    comments_number = serializers.SerializerMethodField()
    gallery = GallerySerializer(many=True)
    authors = ProfileSerializer(many=True)

    class Meta:
        model = Article
        fields = (
            'id', 'alias', 'title', 'text', 'creation_date',
            'publication_date', 'creator', 'authors', 'tags', 'comments_number',
            'gallery')

    def get_comments_number(self, obj):
        return obj.comments.count()


class ArticleSaveSerializer(serializers.ModelSerializer):
    gallery = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Gallery.objects.all())

    class Meta:
        model = Article
        fields = (
        'id', 'alias', 'title', 'text', 'creation_date', 'publication_date',
        'creator', 'tags', 'authors', 'gallery')


"""class ArticleAuthorSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    article = ArticleSerializer()

    class Meta:
        model = ArticleAuthor
        fields = ('id', 'user', 'article')"""


"""class ArticleAuthorSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleAuthor
        fields = ('id', 'user', 'article')"""


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
    is_rented = serializers.SerializerMethodField()

    class Meta:
        model = Hardware
        fields = ('id', 'name', 'description', 'serial_number', 'is_rented')

    def get_is_rented(self, obj):
        return obj.rentals.filter(return_date__isnull=True).exists()


class HardwareSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hardware
        fields = ('id', 'name', 'description', 'serial_number')


class HardwareRentalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    hardware = HardwareSerializer()

    class Meta:
        model = HardwareRental
        fields = ('id', 'rental_date', 'return_date', 'user', 'hardware')


class HardwareRentalSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareRental
        fields = ('id', 'rental_date', 'return_date', 'user', 'hardware')


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'name', 'description', 'isVisible', 'icon')


class ProjectSerializer(serializers.ModelSerializer):
    creator = ProfileSerializer()
    section = SectionSerializer()
    project_authors = ProfileSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'text', 'creation_date', 'publication_date',
                  'repository_link', 'creator', 'section', 'project_authors')


class ProjectSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'text', 'creation_date', 'publication_date',
                  'repository_link', 'creator', 'section')


class ProjectAuthorProjectSerializer(serializers.ModelSerializer):
    creator = ProfileSerializer()
    section = SectionSerializer()

    class Meta:
        model = Project
        fields = ('id', 'title', 'text', 'creation_date', 'publication_date',
                  'repository_link', 'creator', 'section')
