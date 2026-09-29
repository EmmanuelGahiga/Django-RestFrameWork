from rest_framework import serializers
from .models import Post


class PostsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["author", "created_at"]
