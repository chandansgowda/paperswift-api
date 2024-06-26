"""
URL configuration for paperswift_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from core import views as core_views
from paperswift_api import settings
from django_otp.admin import OTPAdminSite

# admin.site.__class__ = OTPAdminSite

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webhook/ci/update-server/', core_views.update_server_webhook),
    path('auth/', include('dj_rest_auth.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs',),
    path('media/question_papers/<path:file_path>',
         core_views.serve_protected_file, name='serve_protected_file'),
    path('management/', include('management.urls')),
    path('assignment/', include('assignment.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
