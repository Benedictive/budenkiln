from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from budenkiln.models import TemperatureCurve
from budenkiln.serializers import TemperaturePointSerializer, TemperatureCurveSerializer
import dbus


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
        bus = dbus.SessionBus()
        remote_object = bus.get_object("de.budenkiln.ControllerService", "/KilnService")
        iface = dbus.Interface(remote_object, "de.budenkiln.ControllerInterface")
        iface.SetCurve(curve.get_points_as_dict())
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
    return  JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getTemperatureHistory(request):
    bus = dbus.SessionBus()
    remote_object = bus.get_object("de.budenkiln.ControllerService", "/KilnService")
    iface = dbus.Interface(remote_object, "de.budenkiln.ControllerInterface")
    temperature_history = dict(iface.GetTempHistory())
    return JsonResponse(temperature_history)