# yourproject/urls.py
from django.contrib import admin
from django.urls import path, include
from yourproject.views import numerical_data_view, FaceDataListCreate, NumericalDataListCreate, MQTTAction

urlpatterns = [
    path('admin/', admin.site.urls),
    path('numericaldata/', numerical_data_view, name='numericaldata'),
    path('facedata/', FaceDataListCreate.as_view(), name='face_data'),
    path('numericaldatalist/', NumericalDataListCreate.as_view(), name='numerical_data_list'),
    path('mqtt-action/', MQTTAction.as_view(), name='mqtt_action'),
    #path('mqtt_integration/', include('mqtt_integration.urls')),
]

