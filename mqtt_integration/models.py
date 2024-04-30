
from django.db import models

class FaceData(models.Model):
    user_id = models.CharField(max_length=255)
    face_encoding = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class NumericalData(models.Model):
    user_id = models.CharField(max_length=255)
    temperature = models.FloatField()
    humidity = models.FloatField()
    gas_level = models.FloatField()
    rain = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

# Create your models here.
