from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=100)
    publication_date = serializers.DateField()

    def create(self, validated_data):
        return Book.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.author = validated_data.get('author',instance.author)
        instance.publication_date = validated_data.get('publication_date',instance.publication_date)
        instance.save()
        return instance