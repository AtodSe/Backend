from rest_framework.serializers import ModelSerializer

from .models import Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'color', 'icon', 'name', 'created_at', 'updated_at']
        read_only_fields = ['updated_at', 'created_at']
