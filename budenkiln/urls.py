from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/setcurve', views.setCurve, name='setcurve'),
]