
from django.urls import path, include
from .views import *

urlpatterns = [
    path('notes/', NoteAPIView.as_view()),
    path('notes/<int:id>', NoteDetails.as_view())
]
