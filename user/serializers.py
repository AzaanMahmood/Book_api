from .models import Author
from rest_framework import serializers
from api.models import Book
class AuthorSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id','name', 'gender','book']
