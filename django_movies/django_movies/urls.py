from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .settings import DEBUG, MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('mainapp.urls')),
    path('', include('authentication.urls')),
]


if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
