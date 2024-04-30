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
from django.core.cache import cache
from django.conf import settings
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
        cached_queryset = cache.get('book_list_queryset')
        if cached_queryset:
            return cached_queryset

        queryset = Book.objects.filter(created_by=self.request.user)
        cache.set('book_list_queryset', queryset, timeout=3600)  # Cache for 1 hour
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class BookRUD(GenericAPIView, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cached_object = cache.get(f'book_{self.kwargs["pk"]}')
        if cached_object:
            return cached_object

        obj = super().get_object()
        if obj.created_by != self.request.user:
            raise PermissionDenied("You do not have permission to access this object.")
        cache.set(f'book_{obj.pk}', obj, timeout=3600) 
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
        cached_queryset = cache.get(f'active_books_by_author_{author_id}')
        if cached_queryset:
            return cached_queryset

        queryset = Book.objects.filter(author_id=author_id, is_active=True)
        cache.set(f'active_books_by_author_{author_id}', queryset, timeout=3600) 
        return queryset

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

        cache.delete(f'book_{book.pk}')

        return Response(status=status.HTTP_201_CREATED)