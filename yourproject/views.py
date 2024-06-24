# mqtt_integration/views.py
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from mqtt_integration.models import FaceData, NumericalData
from mqtt_integration.serializers import FaceDataSerializer, NumericalDataSerializer
from mqtt_integration.publish import publish_message
import logging
import time
import subprocess

logger = logging.getLogger(__name__)

class NumericalDataListCreate(generics.ListCreateAPIView):
    queryset = NumericalData.objects.all()
    serializer_class = NumericalDataSerializer

    def get(self, request, *args, **kwargs):
        # Run the MQTT subscription command
        try:
            process = subprocess.Popen(['python', 'manage.py', 'mqtt_subscribe'])
            process.wait()  # Wait for the process to complete

            # Allow some time for the data to be posted to the API
            time.sleep(5)  # Adjust the sleep time as necessary to ensure data is posted

            # Get the latest data from the database
            latest_data = NumericalData.objects.latest('timestamp')
            return JsonResponse({
                'humidity': latest_data.humidity,
                'temperature_celsius': latest_data.temperature,
                'gas_level': latest_data.gas_level,
                'rain_status': latest_data.rain
            })

        except NumericalData.DoesNotExist:
            return JsonResponse({'error': 'No data available'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error while retrieving data: {e}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FaceDataListCreate(generics.ListCreateAPIView):
    queryset = FaceData.objects.all()
    serializer_class = FaceDataSerializer

class MQTTAction(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        action = request.data.get('action')
        if action == 'mqtt_publish':
            try:
                subprocess.run(['python', 'manage.py', 'mqtt_publish'])
                return Response({'message': 'MQTT publish executed successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error executing MQTT publish: {e}")
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

class PublishAPIView(APIView):
    def post(self, request, *args, **kwargs):
        topic = request.data.get('topic')
        status_message = request.data.get('status')
       # if not topic or not status_message:
          #  return Response({'error': 'Topic and status are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            publish_message(topic, status_message)
            return Response({'message': 'Message published successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error publishing message: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
