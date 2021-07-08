from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('addProductsForSale', products_for_sale),
    path('myProducts', my_products),
    path('myProducts/edit/<int:id>', edit_products),
    path('myProducts/delete/<int:id>', delete_product),
    path('myProducts/editComment', edit_comment),
    path('myProducts/delete/comment/<int:id>', delete_comment),
    path('test/', test),
    path('test/result/', result),
    path('imagetest/', image_test1),
    # path('imagetest_result/', get_image_model)
    # path('test_img', imageTest),
    
]