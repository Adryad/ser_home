# mqtt_integration/views.py
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from mqtt_integration.models import FaceData, NumericalData
from mqtt_integration.serializers import FaceDataSerializer, NumericalDataSerializer
import subprocess
import time

class NumericalDataListCreate(generics.ListCreateAPIView):
    queryset = NumericalData.objects.all()
    serializer_class = NumericalDataSerializer

    def get(self, request, *args, **kwargs):
        # Run the MQTT subscription command
        process = subprocess.Popen(['python', 'manage.py', 'mqtt_subscribe'])
        
        # Wait for the MQTT subscription to complete and gather some data
        process.wait()  # Wait for the process to complete

        # Allow some time for the data to be posted to the API
        time.sleep(5)  # Adjust the sleep time as necessary to ensure data is posted

        # Get the latest data from the database
        try:
            latest_data = NumericalData.objects.latest('timestamp')
        except NumericalData.DoesNotExist:
            return JsonResponse({'error': 'No data available'}, status=status.HTTP_404_NOT_FOUND)

        # Return the retrieved data
        return JsonResponse({
            'humidity': latest_data.humidity,
            'temperature_celsius': latest_data.temperature,
            'gas_level': latest_data.gas_level,
            'rain_status': latest_data.rain
        })

class FaceDataListCreate(generics.ListCreateAPIView):
    queryset = FaceData.objects.all()
    serializer_class = FaceDataSerializer

class MQTTAction(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        action = request.data.get('action')
        if action == 'mqtt_publish':
            subprocess.run(['python', 'manage.py', 'mqtt_publish'])
            return Response({'message': 'MQTT publish executed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
