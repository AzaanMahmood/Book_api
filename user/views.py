from django.shortcuts import render
from .serializers import AuthorSerializer
from .models import Author
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.core.cache import cache
from django.conf import settings

class AuthorListCreate(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cached_queryset = cache.get('author_list_queryset')
        if cached_queryset:
            return cached_queryset

        queryset = Author.objects.all()
        cache.set('author_list_queryset', queryset, timeout=3600) 
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get(self, request, *arg, **kwargs):
        return self.list(request, *arg, **kwargs)

    def post(self, request, *arg, **kwargs):
        return self.create(request, *arg, **kwargs)

class AuthorRUD(GenericAPIView, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cached_object = cache.get(f'author_{self.kwargs["pk"]}')
        if cached_object:
            return cached_object

        obj = super().get_object()
        cache.set(f'author_{obj.pk}', obj, timeout=3600)  
        return obj

    def get_queryset(self):
        return Author.objects.filter(created_by=self.request.user)

    def get(self, request, *arg, **kwargs):
        return self.retrieve(request, *arg, **kwargs)

    def put(self, request, *arg, **kwargs):
        return self.update(request, *arg, **kwargs)

    def delete(self, request, *arg, **kwargs):
        return self.destroy(request, *arg, **kwargs)
    