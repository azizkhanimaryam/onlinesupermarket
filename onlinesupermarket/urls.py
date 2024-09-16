"""
URL configuration for supermarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from products.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("products.urls")),
    #path('products/', include('products.urls', namespace='products')),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('cart/', include('cart.urls')),  # Include cart app URLs
    path('comments/', include('comments.urls')),
    path('users/', include('users.urls',namespace='users')),
    path('', home, name='home'),  # Add this line to define the 'home' URL pattern

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

