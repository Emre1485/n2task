from rest_framework import serializers
from api.models import User,Todo

class TodoSerializer(serializers.ModelSerializer):
    """
    Todo verilerini yonetir.
    
    Frontend tarafinda userId beklendigi icin,   
    DB tarafindaki user alanini `source` argumani ile map'lenir.
    """
    userId = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects.all())
    class Meta:
        model = Todo
        fields = ['userId', 'id', 'title', 'completed']
