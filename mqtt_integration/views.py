from django.http import JsonResponse
from django.core.cache import cache
from rest_framework import generics
from mqtt_integration.models import FaceData, NumericalData
from mqtt_integration.serializers import FaceDataSerializer, NumericalDataSerializer
from rest_framework import status
from rest_framework.response import Response
import threading
import subprocess
# mqtt_integration/views.py
import time
def mqtt_subscribe():
    from mqtt_integration.subscribe import main as mqtt_main
    mqtt_main()

class numerical_data(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        # Start MQTT subscription in a separate thread
        threading.Thread(target=mqtt_subscribe).start()
        
        # Wait for the MQTT subscription to complete and gather some data
        time.sleep(10)  # Adjust the sleep time as necessary to wait for the data

        # Get the data from the cache
        humidity = cache.get('humidity')
        temperature_celsius = cache.get('temperature_celsius')
        gas_level = cache.get('Gas_level')
        rain_status = cache.get('Rain_ST')

        # Check if any data is missing
        if not all([humidity, temperature_celsius, gas_level, rain_status]):
            return JsonResponse({'error': 'Incomplete data'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Return the retrieved data
        return JsonResponse({
            'humidity': humidity,
            'temperature_celsius': temperature_celsius,
            'gas_level': gas_level,
            'rain_status': rain_status
        })

class FaceDataListCreate(generics.ListCreateAPIView):
    queryset = FaceData.objects.all()
    serializer_class = FaceDataSerializer

class NumericalDataListCreate(generics.ListCreateAPIView):
    queryset = NumericalData.objects.all()
    serializer_class = NumericalDataSerializer

class MQTTAction(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        action = request.data.get('action')
        if action == 'mqtt_publish':
            subprocess.run(['python', 'manage.py', 'mqtt_publish'])
            return Response({'message': 'MQTT publish executed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
