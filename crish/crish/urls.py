from django.contrib import admin
from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('crishApp.urls')),
    path('api-auth-token/',obtain_auth_token,name='api_auth_token')
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
