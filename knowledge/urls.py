from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .viewsets import MemoryViewSet, TagViewSet, UserViewSet

app_name = "knowledge"

router = DefaultRouter()
router.register("memory", MemoryViewSet, basename="memory")
router.register("tags", TagViewSet, basename="tags")
router.register("user", UserViewSet, basename="user")

urlpatterns = [

    path('login/', views.obtain_auth_token),

    path('', include(router.urls)),
]
