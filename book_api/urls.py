from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tokenrefresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('Authorapi/', include('user.urls')),
    path('Bookapi/', include('api.urls')),   
    path('', include('api.urls')),
    path('book/', include('api.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
