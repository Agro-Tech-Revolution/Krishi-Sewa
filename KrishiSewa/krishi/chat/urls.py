from django.urls import path 
from . import views

urlpatterns = [
    path('m/<str:username>/', views.room, name='room'),
    path('test/room', views.test)
]