# serializers.py
from rest_framework import serializers
from .models import FaceData, NumericalData

class FaceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceData
        fields = '__all__'

class NumericalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumericalData
        fields = '__all__'

