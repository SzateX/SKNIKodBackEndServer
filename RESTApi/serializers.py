from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Profile, RepoLink, Article, Comment, Tag, ArticleAuthor, \
    ArticleTag, File, HardwareRental, Hardware, Project, ProjectAuthor, Section


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'profile', 'password', 'first_name', 'last_name')
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


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'profile')
        read_only_fields = ('profile', 'groups', 'username')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user')


class RepoLinkSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = RepoLink
        fields = ('id', 'link', 'user')


class RepoLinkSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepoLink
        fields = ('id', 'link', 'user')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ArticleTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer()

    class Meta:
        model = ArticleTag
        fields = ('id', 'tag', 'article')


class ArticleTagSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleTag
        fields = ('id', 'tag', 'article')


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
    tags = ArticleTagSerializer(many=True)
    comments_number = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'alias', 'title', 'text', 'creation_date', 'publication_date', 'creator', 'tags', 'comments_number')

    def get_comments_number(self, obj):
        return obj.comments.count()


class ArticleSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'alias', 'title', 'text', 'creation_date', 'publication_date', 'creator')


class ArticleAuthorSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    article = ArticleSerializer()

    class Meta:
        model = ArticleAuthor
        fields = ('id', 'user', 'article')


class ArticleAuthorSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleAuthor
        fields = ('id', 'user', 'article')


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

    class Meta:
        model = Project
        fields = ('id', 'title', 'text', 'creation_date', 'publication_date', 'repository_link', 'creator', 'section')


class ProjectSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'text', 'creation_date', 'publication_date', 'repository_link', 'creator', 'section')


class ProjectAuthorSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    project = ProjectSerializer()

    class Meta:
        model = ProjectAuthor
        fields = ('id', 'user', 'project')


class ProjectAuthorSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAuthor
        fields = ('id', 'user', 'project')