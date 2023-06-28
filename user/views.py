from django.contrib.auth.models import User, Group
from django.http import Http404
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import Profile
from user.serializers import UserSerializer, UserUpdateSerializer, ProfileSerializer, GroupSerializer
from utils.custom_permissions import IsOwnerOrAdminForUserViewOrReadOnly, IsAdminOrReadOnly


class UserViewSetDetail(APIView):
    queryset = User.objects.none()
    permission_classes = [IsOwnerOrAdminForUserViewOrReadOnly]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        self.check_object_permissions(self.request, queryset)
        serializer = UserSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        self.check_object_permissions(self.request, queryset)
        serializer = UserUpdateSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        self.check_object_permissions(self.request, queryset)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request,  pk=None, format=None):
        queryset = self.get_object(pk)
        self.check_object_permissions(self.request, queryset)
        serializer = UserUpdateSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSetList(APIView):
    queryset = User.objects.none()
    permission_classes = [IsAdminOrReadOnly]

    def get(self, format=None):
        queryset = User.objects.all().order_by('-date_joined')
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSetDetail(APIView):
    queryset = Profile.objects.none()
    permission_classes = [IsOwnerOrAdminForUserViewOrReadOnly]

    def get_object(self, pk=None):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk=pk)
        serializer = ProfileSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ProfileSerializer(queryset, data=request.data)
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
        serializer = ProfileSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSetList(APIView):
    queryset = Profile.objects.none()
    permission_classes = [IsOwnerOrAdminForUserViewOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get(self, request, format=None):
        queryset = Profile.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        if result_page is not None:
            serializer = ProfileSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class GroupViewSetDetail(APIView):
    queryset = Group.objects.none()
    permission_classes = [IsAdminUser]

    def get_object(self, pk=None):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GroupSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GroupSerializer(queryset, data=request.data)
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
        serializer = GroupSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupViewSetList(APIView):
    permission_classes = [IsAdminUser]
    queryset = Group.objects.none()

    def get(self, format=None):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)