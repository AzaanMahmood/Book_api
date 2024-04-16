from django.shortcuts import render
from .serializers import  BookSerializer, ActiveBooksByAuthorSerializer
from .models import Book
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .filter import IsActiveFilter


class BookListCreate(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author']
    filterset_class = IsActiveFilter  # Use the custom filter class here


    def get_queryset(self):
        return Book.objects.fil()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class BookRUD(GenericAPIView, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *arg, **kwargs):
        return self.retrieve(request, *arg, **kwargs)
    
    def put(self, request, *arg, **kwargs):
        return self.update(request, *arg, **kwargs)

    def delete(self, request, *arg, **kwargs):
        return self.destroy(request, *arg, **kwargs)



class ActiveBooksByAuthor(GenericAPIView, ListModelMixin):
    serializer_class = ActiveBooksByAuthorSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        author_id = self.kwargs['author_id']
        return Book.objects.filter(author_id=author_id, is_active=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)