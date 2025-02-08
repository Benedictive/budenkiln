from django.shortcuts import render, get_object_or_404
from django.template import Context
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from budenkiln.models import TemperatureCurve, TemperaturePoint
from budenkiln.serializers import TemperaturePointSerializer, TemperatureCurveSerializer

import zmq
import pickle

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
        curve_points = curve.get_points_as_dict()

        rpc_reply = controller_rpc("set_curve", curve_points)

        return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
    return  JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getTemperatureHistory(request):
    temperature_history = controller_rpc("get_temp_history", None)

    return JsonResponse(temperature_history)

@api_view(['POST'])
def shutdownBudenkiln(request):
    controller_rpc("shutdown_kiln", None)
    return HttpResponse(status=status.HTTP_200_OK)

def controller_rpc(method, content):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    message = create_rpc_message(method, content)
    serialized_message = pickle.dumps(message)

    socket.send(serialized_message)

    serialized_reply = socket.recv()
    return pickle.loads(serialized_reply)

def create_rpc_message(remote_procedure, content):
    return (remote_procedure, content)