from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/curve', views.setCurve, name='apicurve'),
    path('api/curve/<name>', views.setPoint, name='apipoint'),
]