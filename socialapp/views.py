from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from socialapp.models import Post
from socialapp.serializer import PostSerializer, PostDetailSerializer


class PostListCreateView(APIView):
    """ Get list of objects or Create new one """

    def get(self, request, format=None):
        # Get all post objects, serialize them and return to user
        obj = Post.objects.all()
        serializer = PostSerializer(obj, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # Get title and text from request.data and author from request.user.id
        data = {
            'author': request.user.id,
            'title': request.data['title'],
            'text': request.data['text']
        }
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """ Retrieve, update or delete object """
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)


class LikeListCreateView(APIView):
    """ Get list or statistics of objects or Create new one """
    pass


class LikeDetailView(APIView):
    """ Retrieve, update or delete object """
    pass
