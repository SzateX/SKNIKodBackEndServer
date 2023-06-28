from django.contrib.auth.models import User
from rest_framework import serializers

from links.models import GenericLink
from links.serializers import GenericLinkSerializer
from user.models import Profile
from user.serializers import ShortUserSerializer, ProfileSerializer
from .models import Article, Comment, Tag, \
    File, HardwareRental, Hardware, Project, \
    Sponsor, Section, Gallery, FooterLink

from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField


class GallerySerializer(serializers.ModelSerializer):
    thumbnail = HyperlinkedSorlImageField(
        '512x512',
        options={"crop": "center"},
        source='image',
        read_only=True
    )

    class Meta:
        model = Gallery
        fields = ('id', 'image', 'thumbnail', 'thumbnail_visibility', 'text_visibility', 'gallery_visibility')


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
    links = GenericLinkSerializer(many=True)

    class Meta:
        model = Article
        fields = (
            'id', 'alias', 'title', 'text', 'creation_date', 'group',
            'publication_date', 'creator', 'authors', 'tags', 'comments_number',
            'gallery', 'links')

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
        return super(CommentSaveSerializer, self).validate(data)


class ArticleSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'id', 'alias', 'title', 'text', 'group', 'creation_date', 'publication_date',
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
        fields = ('id', 'name', 'description', 'serial_number', 'status')


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


class ProjectSerializer(serializers.ModelSerializer):
    creator = ShortUserSerializer()
    section = SectionSerializer()
    authors = ShortUserSerializer(many=True)
    links = GenericLinkSerializer(many=True)
    gallery = GallerySerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'text', 'creation_date', 'publication_date', 'creator', 'section', 'authors', 'gallery', 'links')


class ProjectSaveSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(many=True, required=True, queryset=User.objects.all())

    class Meta:
        model = Project
        fields = ('id', 'title', 'text', 'creation_date', 'publication_date', 'creator', 'section', 'authors', 'gallery')
        extra_kwargs = {'gallery': {'required': False}}


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ('id', 'name', 'logo', 'url')


class GenericLinkObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Article):
            serializer = ArticleSerializer(value)
        elif isinstance(value, Profile):
            serializer = ProfileSerializer(value)
        elif isinstance(value, Project):
            serializer = ProjectSerializer(value)
        else:
            raise Exception("Unknown type of object")
        return serializer.data


class GenericLinkBigSerializer(serializers.ModelSerializer):
    linked_object = GenericLinkObjectRelatedField(read_only=True)

    class Meta:
        model = GenericLink
        fields = ('id', 'link', 'link_type', 'linked_object', 'content_type')


class GenericLinkBigSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericLink
        fields = ('id', 'link', 'link_type', 'linked_object', 'content_type')


class FooterLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLink
        fields = ('id', 'link', 'title', 'icon', 'color')
