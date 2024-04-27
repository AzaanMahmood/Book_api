from django.contrib import admin
from django.urls import path
from api import views
from api.views import BookImageUpload


urlpatterns = [
    path('',views.BookListCreate.as_view()),
    path('<int:pk>/',views.BookRUD.as_view()),
    path('<int:author_id>/', views.BookListCreate.as_view(), name='books_by_author'),
    path('active_books_by_author/<int:author_id>/', views.ActiveBooksByAuthor.as_view(), name='active-books-by-author'),
    path('upload-image/<int:pk>/', BookImageUpload.as_view(), name='book-image-upload'),


]