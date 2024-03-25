from django.shortcuts import render
from .serializers import  BookSerializer
from .models import Book
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


class BookListCreate(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *arg, **kwargs):
        return self.list(request, *arg, **kwargs)
    
    def post(self, request, *arg, **kwargs):
        return self.create(request, *arg, **kwargs)

class BookRUD(GenericAPIView, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *arg, **kwargs):
        return self.retrieve(request, *arg, **kwargs)
    
    def put(self, request, *arg, **kwargs):
        return self.update(request, *arg, **kwargs)

    def delete(self, request, *arg, **kwargs):
        return self.destroy(request, *arg, **kwargs)
