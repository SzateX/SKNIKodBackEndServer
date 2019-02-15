from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Profile, RepoLink, Article, Comment, Tag, ArticleAuthor, \
    ArticleTag, File, HardwareRental, Hardware, Project, ProjectAuthor, Section


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'profile', 'password')
        read_only_fields = ('profile', 'groups')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ArticleTagSerializer(serializers.ModelSerializer):
    class _ArticleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = (
                'id', 'title', 'text', 'creation_date', 'publication_date',
                'creator')

    tag = TagSerializer()
    article = _ArticleSerializer()

    class Meta:
        model = ArticleTag
        fields = ('id', 'tag', 'article')


class ArticleSerializer(serializers.ModelSerializer):
    creator = ProfileSerializer()
    tags = ArticleTagSerializer()

    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'creation_date', 'publication_date', 'creator', 'tags')


class CommentSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'creation_date', 'article', 'user')


class ArticleAuthorSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    article = ArticleSerializer()

    class Meta:
        model = ArticleAuthor
        fields = ('id', 'user', 'article')


class FileSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    article = ArticleSerializer()

    class Meta:
        model = File
        fields = ('id', 'creation_date', 'user', 'article')


class HardwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hardware
        fields = ('id', 'name', 'description')


class HardwareRentalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    hardware_piece = HardwareSerializer()

    class Meta:
        model = HardwareRental
        fields = ('id', 'rental_date', 'return_date', 'user', 'hardware_piece')


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'name', 'description', 'isVisible')


class ProjectSerializer(serializers.ModelSerializer):
    creator = ProfileSerializer()
    section = SectionSerializer()

    class Meta:
        model = Project
        fields = ('id', 'title', 'text', 'creation_date', 'publication_date', 'repository_link', 'creator', 'section')


class ProjectAuthorSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    project = ProjectSerializer()

    class Meta:
        model = ProjectAuthor
        fields = ('id', 'user', 'project')