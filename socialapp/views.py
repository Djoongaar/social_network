import django_filters
from django.db.models import Count
from django.http import Http404

from django_filters import rest_framework as filters

from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from socialapp.models import Post, Like
from socialapp.serializer import PostSerializer, PostDetailSerializer, LikeSerializer, LikeAnalyticSerializer


class PostListCreateView(APIView):
    """ Get list of objects or Create new one """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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


class LikeCreateDestroyView(APIView):
    """ Like / Unlike """

    def get_object(self, pk, request):
        """ Getting object by filtering Like obj by post_id, then get unique by user.id """
        try:
            post = Like.objects.filter(post_id=pk).get(user_id=request.user.id)
            return post
        except Like.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        like_obj = self.get_object(pk, request)
        if like_obj:
            # if Like object already exist --> delete obj
            like_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            #  Otherwise Create the New One
            data = {
                'user': request.user.id,
                'post': pk
            }
            serializer = LikeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeFilterSet(filters.FilterSet):
    """ Create specific filters """
    date_from = filters.DateFilter(field_name='created', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='created', lookup_expr='lte')

    class Meta:
        model = Like
        fields = ('date_from', 'date_to')


class LikeList(generics.ListAPIView):
    """ Get and aggregate queryset and filter it by FilterSet """
    queryset = Like.objects.all().values('created').annotate(total=Count('created'))
    serializer_class = LikeAnalyticSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LikeFilterSet

