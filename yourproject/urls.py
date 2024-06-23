"""yourproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from .views import FaceDataListCreate, NumericalDataListCreate, MQTTAction, PublishAPIView
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('facedata/', FaceDataListCreate.as_view(), name='facedata-list-create'),
    #path('numericaldata/', NumericalDataListCreate.as_view(), name='numericaldata-list-create'),
    #path('mqtt/', MQTTAction.as_view(), name='mqtt-action'),
]
urlpatterns = [
    path('facedata/', FaceDataListCreate.as_view(), name='facedata-list-create'),
    path('numericaldata/', NumericalDataListCreate.as_view(), name='numericaldata-list-create'),
    path('mqtt/', MQTTAction.as_view(), name='mqtt-action'),
    path('publish/', PublishAPIView.as_view(), name='publish-api'),
    #path('', RedirectView.as_view(url='facedata/', permanent=False)),
    path('', RedirectView.as_view(url='numericaldata/', permanent=False)),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)