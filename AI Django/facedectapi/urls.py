from django.contrib import admin
from django.urls import path, include
from facedectapi import views

urlpatterns = [
    path('validate', views.valid, name="valid"),
    path('register', views.insert, name="insert"),
    path('logging', views.log, name="log"),
    path('identify', views.identify, name="identify"),
    path('training', views.traine, name="training"),
]