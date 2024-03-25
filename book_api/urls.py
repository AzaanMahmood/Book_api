from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Authorapi/', include('user.urls')),
    path('Bookapi/', include('api.urls')),
]
