"""djangoxtermjs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url, include
from xterm import views as xterms_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', xterms_views.index, name='index'),

    path('images/', xterms_views.images, name='images'),
    path('ajaxImages/', xterms_views.ajaxImages, name='ajaxImages'),

    path('containers/', xterms_views.containers, name='containers'),
    path('ajaxContainers/', xterms_views.ajaxContainers, name='ajaxContainers'),


    path('console/<slug:id>/', xterms_views.console, name='console'),
    path('start_stop_remove/', xterms_views.start_stop_remove, name='start_stop_remove'),
    path('removeImage/', xterms_views.removeImage, name='removeImage'),
    path('runImage/', xterms_views.runImage, name='runImage'),
    path('browse/', xterms_views.browse, name='browse'),

    path('get_progress/<slug:task_id>/', xterms_views.get_progress, name='get_progress'),


]+    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

