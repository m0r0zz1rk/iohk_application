from django.contrib import admin
from django.urls import path, include

from .vars.yasg import urlpatterns as yasg_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.authen.urls')),
    path('api/v1/admins/', include('apps.admins.urls'))
]
urlpatterns += yasg_urls
