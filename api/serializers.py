from .models import Book
from rest_framework import serializers
from user.models import Author

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    class Meta:
        model = Book
        fields = ['id','title', 'author', 'publication_date', 'author_name']

