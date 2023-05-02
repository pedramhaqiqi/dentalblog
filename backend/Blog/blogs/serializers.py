from rest_framework import serializers
from blogs.models import BlogModel


class BlogsSerializer(serializers.Serializer):
    class Meta:
        model = BlogModel
        fields = ("summary", "title", "source_url", "image_url")