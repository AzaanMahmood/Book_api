from django.contrib import admin
from django.urls import path
from api import views


urlpatterns = [
    path('',views.BookListCreate.as_view()),
    path('<int:pk>/',views.BookRUD.as_view()),
]