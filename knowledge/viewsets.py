from django.db.models import Q
from rest_framework import viewsets, filters, serializers, mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .utils import get_object, add_user_to_data, chain_filter
from .serializers import MemorySerializer, TagSerializer, TagList, UserSerializer
from .models import Memory, Tag, RegularUser


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]


class MemoryViewSet(BaseViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = MemorySerializer
    search_fields = ['memory_text', ]
    ordering = ['-priority']

    class Meta:
        model = Memory

    def get_queryset(self):
        return Memory.objects.filter(user=self.request.user).prefetch_related('tags')

    def create(self, request, *args, **kwargs):
        add_user_to_data(request)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        add_user_to_data(request)
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)


class TagViewSet(BaseViewSet):
    search_fields = ['tag_text']
    ordering = ['-count']
    serializer_class = TagSerializer

    class Meta:
        model = Tag

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    @action(url_name='search_memory', url_path='search_memory', detail=False, methods=['post', ])
    def search_memory_by_tags(self, request):
        add_user_to_data(request)
        serializer = TagList(data=request.data)
        if serializer.is_valid(raise_exception=True):
            tag_q = [Q(tags=tag) for tag in serializer.validated_data['tags']]
            res = chain_filter(Memory, tag_q, user=request.user)
            memory = MemorySerializer(instance=res, many=True)
            return Response(memory.data)


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  GenericViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        return RegularUser.objects.filter(id=self.kwargs['pk'])

    class Meta:
        model = RegularUser
