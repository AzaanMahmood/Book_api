from django.urls import path
from . import views as b

urlpatterns = [
    path('books/', b.book_list),
    path('books/<int:pk>/', b.book_detail),
]
