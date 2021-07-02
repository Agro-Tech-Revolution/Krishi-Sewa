from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('addProducts', products),
    path('myProducts', my_products),
    path('myProducts/edit/<int:id>', edit_products),
    path('myProducts/delete/<int:id>', delete_product),
    path('myProducts/editComment', edit_comment),
    path('myProducts/delete/comment/<int:id>', delete_comment),
    path('test/', test),
    path('test/result/', result),
    path('imagetest', image_test),
    
]