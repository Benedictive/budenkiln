from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from budenkiln.models import TemperatureCurve
from budenkiln.serializers import TemperaturePointSerializer, TemperatureCurveSerializer, KilnSerializer
from hardware_controller import set_temp_curve


# Create your views here.
def index(request):
    return render(request, 'budenkiln/index.html')

@api_view(['POST'])
def setCurve(request):
    serializer = TemperatureCurveSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def setPoint(request, name):
    print("SetPoint request for curve {}".format(name))
    try:
        curve = TemperatureCurve.objects.get(name=name)
    except:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    serializer = TemperaturePointSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save(curve=curve)
        set_temp_curve(curve)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
    return  JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)