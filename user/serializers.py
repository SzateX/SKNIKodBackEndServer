from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User, Group
from rest_framework import serializers

from links.serializers import GenericLinkSerializer
from user.models import Profile


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
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'profile', 'password',
                  'first_name', 'last_name', 'is_admin_user', 'permissions')
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

    def get_permissions(self, obj):
        all_permissions = filter(lambda x: x.startswith('rest_api') or x.startswith('auth') and not x.startswith('authtoken'), User(is_superuser=True).get_all_permissions())
        user_permissions = obj.get_all_permissions()

        return {p: p in user_permissions for p in all_permissions}


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
    links = GenericLinkSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'description', 'avatar', 'index_number', 'links')


class ProfileWithoutUserSerializer(serializers.ModelSerializer):
    links = GenericLinkSerializer(many=True)

    class Meta:
        model = Profile
        fields = ('id', 'description', 'links', 'index_number')


class ShortUserSerializer(serializers.ModelSerializer):
    profile = ProfileWithoutUserSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile')