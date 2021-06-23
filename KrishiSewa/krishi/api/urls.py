
from django.urls import path, include
from .views import *

urlpatterns = [
    path('notes/', NoteAPIView.as_view()),
    path('notes/<int:id>', NoteDetails.as_view()),
    path('users/', UserAPIView.as_view()),
    path('users/<str:username>', UserDetail.as_view()),
    path('profile/', CreateProfile.as_view()),
    path('profile/<int:user_id>', GetProfileType.as_view()),
]
