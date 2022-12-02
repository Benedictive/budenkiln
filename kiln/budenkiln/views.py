from django.shortcuts import render, get_object_or_404
from django.template import Context
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from budenkiln.models import TemperatureCurve, TemperaturePoint
from budenkiln.serializers import TemperaturePointSerializer, TemperatureCurveSerializer

import zmq

# Create your views here.
def index(request):
    existing_curves = TemperatureCurve.objects.all()
    context = {"existing_curves": existing_curves}
    return render(request, 'budenkiln/index.html', context)

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
    curve = get_object_or_404(TemperatureCurve, name=name)

    serializer = TemperaturePointSerializer(data=request.data, many=True)
    if serializer.is_valid():
        # Remove old points and override with new if valid
        old_points = TemperaturePoint.objects.filter(curve=curve)
        old_points.delete()

        serializer.save(curve=curve)

        context = zmq.Context()

        print("Conn")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")

        for req in range(10):
            print("Sending {}".format(req))
            socket.send(b"Hello")

            message = socket.recv()
            print("Rec {} : {}".format(req, message))
        #getBudenkilnDBusInterface().SetCurve(curve.get_points_as_dict())

        return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
    return  JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getTemperatureHistory(request):
    print("Getting History")
    temperature_history = {0:1}

    return JsonResponse(temperature_history)

@api_view(['POST'])
def shutdownBudenkiln(request):
    #getBudenkilnDBusInterface().ShutdownKiln()
    return HttpResponse(status=status.HTTP_200_OK)