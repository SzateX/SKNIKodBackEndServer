from links.models import GenericLink
from rest_framework import serializers


class GenericLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericLink
        fields = ('id', 'link', 'link_type')
