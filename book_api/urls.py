from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tokenrefresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('Authorapi/', include('user.urls')),
    path('Bookapi/', include('api.urls')),
]
