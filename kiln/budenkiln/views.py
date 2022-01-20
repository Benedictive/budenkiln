from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from budenkiln.models import TemperaturePoint, TemperatureCurve, Kiln
from budenkiln.serializers import TemperaturePointSerializer, TemperatureCurveSerializer, KilnSerializer

# Create your views here.
def index(request):
    return render(request, 'budenkiln/index.html')

@csrf_exempt
def setCurve(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TemperatureCurveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return  JsonResponse(serializer.errors, status=400)