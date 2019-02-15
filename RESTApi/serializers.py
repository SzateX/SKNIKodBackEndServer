from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Profile, RepoLink, Article, Comment, Tag, ArticleAuthor, \
    ArticleTag, File, ArticleType, HardwareRental, HardwarePiece, Hardware, AboutData


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
        fields = ('id', 'technologies', 'interests', 'user')


class RepoLinkSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = RepoLink
        fields = ('id', 'link', 'user')


class ArticleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleType
        fields = ('id', 'name')


class ArticleSerializer(serializers.ModelSerializer):
    article_type = ArticleTypeSerializer()
    creator = ProfileSerializer()

    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'creation_date', 'publication_date',
                  'article_type', 'repository_link', 'creator')


class CommentSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'creation_date', 'parent_comment', 'article',
                  'user')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'id', 'name')


class ArticleAuthorSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    article = ArticleSerializer()

    class Meta:
        model = ArticleAuthor
        fields = ('id', 'user', 'article')


class ArticleTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    article = ArticleSerializer()

    class Meta:
        model = ArticleTag
        fields = ('id', 'tag', 'article')


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


class HardwarePieceSerializer(serializers.ModelSerializer):
    hardware = HardwareSerializer()

    class Meta:
        model = HardwarePiece
        fields = ('id', 'hardware')


class HardwareRentalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    hardware_piece = HardwareSerializer()

    class Meta:
        model = HardwareRental
        fields = ('id', 'rental_date', 'return_date', 'user', 'hardware_piece')


class AboutDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutData
        fields = ('id', 'title', 'content', 'isVisible')