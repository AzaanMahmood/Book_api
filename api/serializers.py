from .models import Book
from rest_framework import serializers
from user.models import Author

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ['id','title', 'author', 'publication_date', 'author_name', 'created_by', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class ActiveBooksByAuthorSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Book
        fields = ['title', 'author_name']

class BookImageSerializer(serializers.Serializer):
    image = serializers.ImageField()