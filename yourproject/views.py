from django.shortcuts import render
from rest_framework import generics
#from ..mqtt_integration.models import FaceData, NumericalData
#from ..mqtt_integration.serializers import FaceDataSerializer, NumericalDataSerializer
from mqtt_integration.models import FaceData, NumericalData
from mqtt_integration.serializers import FaceDataSerializer, NumericalDataSerializer



class FaceDataListCreate(generics.ListCreateAPIView):
    queryset = FaceData.objects.all()
    serializer_class = FaceDataSerializer

class NumericalDataListCreate(generics.ListCreateAPIView):
    queryset = NumericalData.objects.all()
    serializer_class = NumericalDataSerializer
# views.py
from rest_framework import generics, status
from rest_framework.response import Response
import subprocess

class MQTTAction(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        action = request.data.get('action')
        if action == 'mqtt_publish':
            # Execute MQTT publish command
            subprocess.run(['python', 'manage.py', 'mqtt_publish'])
            return Response({'message': 'MQTT publish executed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
