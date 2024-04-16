import django_filters
from .models import Book

class IsActiveFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'is_active': ['exact'],
        }