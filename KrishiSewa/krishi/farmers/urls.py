from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
<<<<<<< HEAD
    path('addProducts', products),
    path('myProducts', my_products),
    path('myProducts/edit/<int:id>', edit_products),
    path('myProducts/delete/<int:id>', delete_product),
    path('myProducts/editComment', edit_comment),
    path('myProducts/delete/comment/<int:id>', delete_comment),
=======
    path('test/', test),
    path('test/result/', result),
>>>>>>> 60329d801254211da2af477d781c56d9668430e4
    
]