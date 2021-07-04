from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView


class PostListCreateView(APIView):
    """ Get list of objects or Create new one """
    pass


class PostDetailView(APIView):
    """ Retrieve, update or delete object """
    pass


class LikeListCreateView(APIView):
    """ Get list or statistics of objects or Create new one """
    pass


class LikeDetailView(APIView):
    """ Retrieve, update or delete object """
    pass
