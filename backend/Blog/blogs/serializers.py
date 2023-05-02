from rest_framework import serializers
from blogs.models import BlogModel


class BlogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogModel
        fields = ("summary", "title", "source_url")