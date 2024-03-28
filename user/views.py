from django.shortcuts import render
from .serializers import AuthorSerializer
from .models import Author
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated


class AuthorListCreate(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *arg, **kwargs):
        return self.list(request, *arg, **kwargs)
    
    def post(self, request, *arg, **kwargs):
        return self.create(request, *arg, **kwargs)

class AuthorRUD(GenericAPIView, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


    def get(self, request, *arg, **kwargs):
        return self.retrieve(request, *arg, **kwargs)
    
    def put(self, request, *arg, **kwargs):
        return self.update(request, *arg, **kwargs)

    def delete(self, request, *arg, **kwargs):
        return self.destroy(request, *arg, **kwargs)
    