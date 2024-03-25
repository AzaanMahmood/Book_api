from django.contrib import admin
from django.urls import path
from user import views


urlpatterns = [
    path('',views.AuthorListCreate.as_view()),
    path('<int:pk>/',views.AuthorRUD.as_view()),
]