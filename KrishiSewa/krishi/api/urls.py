
from django.urls import path, include
from .views import *

urlpatterns = [
    path('users/', UserAPIView.as_view()),
    path('users/<str:username>', UserDetail.as_view()),
    path('profile/', CreateProfile.as_view()),
    path('profile/<int:user_id>', GetProfileType.as_view()),
    path('notes/', NoteAPIView.as_view()),
    path('notes/<int:id>', NoteDetails.as_view()),
    path('products/', ProductAPIView.as_view()),
    path('products/mine/<int:user_id>', MyProducts.as_view()),
    path('products/<int:prod_id>', ProductDetails.as_view()),
    
]
