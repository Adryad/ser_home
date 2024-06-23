# mqtt_integration/views.py
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from mqtt_integration.models import FaceData, NumericalData
from mqtt_integration.serializers import FaceDataSerializer, NumericalDataSerializer
import subprocess
from mqtt_integration.publish import publish_message
import logging

logger = logging.getLogger(__name__)

class NumericalDataListCreate(generics.ListCreateAPIView):
    queryset = NumericalData.objects.all()
    serializer_class = NumericalDataSerializer

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

class PublishAPIView(APIView):
    def post(self, request, *args, **kwargs):
        logger.debug("Received data: %s", request.data)  # Debug line

        topic = request.data.get('topic')
        status_message = request.data.get('status')
        if not topic or not status_message:
            return Response({'error': 'Topic and status are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            publish_message(topic, status_message)
            return Response({'message': 'Message published successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
