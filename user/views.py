from django.shortcuts import render
from .serializers import AuthorSerializer
from .models import Author
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class AuthorListCreate(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Author.objects.filter(created_by=self.request.user, is_active=True)

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
        obj = super().get_object()
        user = self.request.user
        if obj.created_by != user:
            raise PermissionDenied("You do not have permission to access this object.")
        return obj

    def get_queryset(self):
        return Author.objects.filter(created_by=self.request.user)

    def get(self, request, *arg, **kwargs):
        return self.retrieve(request, *arg, **kwargs)

    def put(self, request, *arg, **kwargs):
        return self.update(request, *arg, **kwargs)

    def delete(self, request, *arg, **kwargs):
        return self.destroy(request, *arg, **kwargs)
    