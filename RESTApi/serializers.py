from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Profile, RepoLink, Article, Comment, Tag, ArticleAuthor, \
    ArticleTag, File, ArticleType, HardwareRental, HardwarePiece, Hardware


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'profile', 'password')
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


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('url', 'technologies', 'interests', 'user')


class RepoLinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RepoLink
        fields = ('url', 'link', 'user')


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ('url', 'title', 'text', 'creation_date', 'publication_date',
                  'article_type', 'repository_link', 'creator')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('url', 'text', 'creation_date', 'parent_comment', 'article',
                  'user')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('url', 'id', 'name')


class ArticleAuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArticleAuthor
        fields = ('url', 'user', 'article')


class ArticleTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArticleTag
        fields = ('url', 'tag', 'article')


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ('url', 'creation_date', 'user', 'article')


class ArticleTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArticleType
        fields = ('url', 'name')


class HardwareRentalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HardwareRental
        fields = ('url', 'rental_date', 'return_date', 'user', 'hardware_piece')


class HardwarePieceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HardwarePiece
        fields = ('url', 'hardware')


class HardwareSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hardware
        fields = ('url', 'name', 'description')
