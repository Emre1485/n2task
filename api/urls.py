from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, PostViewSet, CommentViewSet, AlbumViewSet, PhotoViewSet, TodoViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'photos', PhotoViewSet)
router.register(r'todos', TodoViewSet)

urlpatterns = router.urls