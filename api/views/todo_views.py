from rest_framework import viewsets, filters
from api.models.todos import Todo
from api.serializers.todo_serializers import TodoSerializer 
from django_filters.rest_framework import DjangoFilterBackend

class TodoViewSet(viewsets.ModelViewSet):
    """
    Todo işlemlerini yöneten ViewSet
    
    Bu endpoint üzerinden:
    - Tüm görevler listelenebilir.
    - `completed=true` veya `completed=false` ile duruma göre filtreleme yapilabilir.
    - `user={id}` parametresi ile belli bir kullanicinin görevleri sorgulanabilir.
    - Yeni görev oluşturulabilir, düzenlenebilir, sililnebilir.
    """
    queryset = Todo.objects.all().order_by('-id')
    serializer_class = TodoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'completed']
    search_fields = ['title']
    ordering_fields = ['completed', 'id', 'title']
    