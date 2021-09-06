
from django.urls import path
from .views import *


urlpatterns = [
    path('', home),
    path('login/', login_view),
    path('register', register_view),
    path('history', history),
    path('feedback', feedback),
    path('logout', logout_user),
    path('reportuser/<int:user_id>/', report_user),
    path('send-response/<int:ticket_id>/', send_response),
]

