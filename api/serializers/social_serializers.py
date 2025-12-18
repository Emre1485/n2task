from rest_framework import serializers
from api.models.social import User, Post, Comment, Album, Photo


class PostSerializer(serializers.ModelSerializer):
    """
    Post verilerini isler.

    Frontend tarafinda userId beklendigi icin,  
    DB tarafindaki user alanini `source` argumani ile map'lenir.
    """
    userId = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects.all())
    class Meta:
        model = Post
        fields = ['userId', 'id', 'title', 'body']

class CommentSerializer(serializers.ModelSerializer):
    """
    Yorum islemleri icin kullanilir.

    postId alani, iliskisel oldugu Post objesini isaret eder.
    """
    postId = serializers.PrimaryKeyRelatedField(source='post', queryset=Post.objects.all())
    class Meta:
        model = Comment
        fields = ['postId', 'id', 'name', 'email', 'body']

class PostWithCommentsSerializer(serializers.ModelSerializer):
    """
    Post detayini ve altindaki yorumlari birlikte doner.  
    Read only amaclidir.
    """
    userId = serializers.IntegerField(source='user_id', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['userId', 'id', 'title', 'body', 'comments']

class AlbumSerializer(serializers.ModelSerializer):
    """
    Album verilerini yonetir.
    
    Frontend'den gelen 'userId' alanini, veritabanindaki 'user' iliskisiyle   
    eslestirmek icin source parametresi kullanilir.
    """
    userId = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects.all())
    class Meta:
        model = Album
        fields = ['userId', 'id', 'title']

class PhotoSerializer(serializers.ModelSerializer):
    """
    Fotograf verilerini yonetir.  
    thumbnailUrl (frontend) -> thumbnail_url (backend) donusumu yapilir.
    """
    albumId = serializers.PrimaryKeyRelatedField(source='album', queryset=Album.objects.all())
    thumbnailUrl = serializers.URLField(source='thumbnail_url')
    class Meta:
        model = Photo
        fields = ['albumId', 'id', 'title', 'url', 'thumbnailUrl']


class AlbumWithPhotosSerializer(serializers.ModelSerializer):
    """
    Album detayini icindeki fotograflarla birlikte (Nested) getirir.
    """
    userId = serializers.IntegerField(source='user_id', read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)
    class Meta:
        model = Album
        fields = ['userId', 'id', 'title', 'photos']