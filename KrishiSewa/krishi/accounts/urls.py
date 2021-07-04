
from django.urls import path
from .views import *


urlpatterns = [
    path('', home),
    path('login', login_view),
    path('register', register_view),
    path('history', history),
    path('feedback', feedback),
    path('logout', logout_user),
    
]

