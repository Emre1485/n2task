from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models.accounts import User
from api.serializers.account_serializers import UserSerializer


from api.serializers import PostSerializer, AlbumSerializer, TodoSerializer

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class UserViewSet(viewsets.ModelViewSet):
    """
    - `select_related` kullanilarak Address, Geo ve Company tablolari tek sorguda cekilir.  
    - Kullanici profiline bagli alt kaynaklara (Posts, Albums, Todos) erisim icin ozel actionlar tanimlanmistir.  
    """
    queryset = User.objects.all().select_related('address__geo', 'company')
    serializer_class = UserSerializer
    
    @method_decorator(cache_page(60*1))
    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """
        Kullaniciya ait gonderileri listeler.
        """
        user = self.get_object()
        posts = user.posts.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    @method_decorator(cache_page(60*1))
    @action(detail=True, methods=['get'])
    def albums(self, request, pk=None):
        """
        Kullaniciya ait albumleri listeler.
        """
        user = self.get_object()
        albums = user.albums.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['get'])
    def todos(self, request, pk=None):
        """
        Kullaniciya ait gorevleri listeler.
        Todo islemlerinde sık yazma yapilabilir diye  
        cacheleme devre dısı.
        """
        user = self.get_object()
        todos = user.todos.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)