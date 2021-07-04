from rest_framework import serializers
from socialapp.models import Post, Like


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'text', 'author']


class PostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'count_likes']


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['user', 'post']
