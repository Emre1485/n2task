from rest_framework import viewsets
from api.models.social import Post, Comment, Album, Photo
from api.serializers.social_serializers import PostSerializer, CommentSerializer, AlbumSerializer, PhotoSerializer 
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60*1), name='list')
@method_decorator(cache_page(60*3), name='retrieve')
class PostViewSet(viewsets.ModelViewSet):
    """Gonderi islemlerini yonetir."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

@method_decorator(cache_page(60*1), name='list')
@method_decorator(cache_page(60*3), name='retrieve')
class CommentViewSet(viewsets.ModelViewSet):
    """Yorum islemlerini yonetir."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'email']

@method_decorator(cache_page(60*3), name='list')
@method_decorator(cache_page(60*5), name='retrieve')
class AlbumViewSet(viewsets.ModelViewSet):
    """Album islemlerini yonetir."""
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

@method_decorator(cache_page(60*3), name='list')
@method_decorator(cache_page(60*5), name='retrieve')
class PhotoViewSet(viewsets.ModelViewSet):
    """Fotograf islemlerini yonetir."""
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['album']

