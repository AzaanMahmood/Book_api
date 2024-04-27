from django.shortcuts import render
from .serializers import  BookSerializer, ActiveBooksByAuthorSerializer, BookImageSerializer
from .models import Book
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status

from .filter import IsActiveFilter


class BookListCreate(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author']
    filterset_class = IsActiveFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return Book.objects.filter(created_by=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class BookRUD(GenericAPIView, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if obj.created_by != user:
            raise PermissionDenied("You do not have permission to access this object.")
        return obj

    def get_queryset(self):
        return Book.objects.filter(created_by=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class ActiveBooksByAuthor(GenericAPIView, ListModelMixin):
    serializer_class = ActiveBooksByAuthorSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        author_id = self.kwargs['author_id']
        return Book.objects.filter(author_id=author_id, is_active=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    


class BookImageUpload(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all() 
    serializer_class = BookImageSerializer

    def perform_update(self, serializer):
        serializer.save(image=self.request.data.get('image'))

        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data['image']
        book = self.get_object() 
        book.image = image
        book.save()
        return Response(status=status.HTTP_201_CREATED)