"""tinymce_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from tinymce_demo.views import image_upload, NewsViewSet, TinyMCEPictureViewSet

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('tinymce/', include('tinymce.urls')),
    path('tinymce_image_upload/', image_upload),  # the URL for image upload
    path('api/v1/tinymce-picture/', TinyMCEPictureViewSet.as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/v1/news', NewsViewSet.as_view({'get': 'list'})),
)
