from rest_framework import serializers
from budenkiln.models import TemperaturePoint, TemperatureCurve, Kiln

class KilnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kiln
        fields = '__all__'

class TemperatureCurveSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureCurve
        fields = '__all__'

class TemperaturePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperaturePoint
        fields = ['time', 'temperature']