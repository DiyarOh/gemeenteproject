"""
URL configuration for klachtapp project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from klachtsysteem.views import HomePageView, login_view, register_view, invalid_code_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(HomePageView.as_view()), name='home'),
    path('klacht/', include('klachtsysteem.urls')),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register_no_code'),
    path('register/<str:invitation_code>/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    path('invalid_code/', invalid_code_view, name='invalid_code')
]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)