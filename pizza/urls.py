# -*- Mode: Python; coding: utf-8 -*-
from django.contrib.auth.decorators import permission_required
from django.conf.urls import *
from django.contrib import admin
from pizza.views import *
from django.contrib.staticfiles import views
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.conf import settings
from . import views
# from django.contrib.auth.views import login
from django.contrib.auth import views as auth_views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # Inicio

    # Fim Inicio
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'', include('core.urls', namespace='core')),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
