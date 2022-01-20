from rest_framework import serializers
from budenkiln.models import TemperaturePoint, TemperatureCurve, Kiln

class KilnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kiln
        fields = ['last_curve']

class TemperatureCurveSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureCurve
        fields = ['name']

class TemperaturePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperaturePoint
        fields = ['curve', 'time', 'temperature']