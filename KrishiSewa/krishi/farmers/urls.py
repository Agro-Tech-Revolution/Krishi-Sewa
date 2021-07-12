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

    path('addProduction', add_production),
    path('editProduction/<int:id>', edit_production),
    path('deleteProduction/<int:id>', delete_production),
    
    path('sellProduct', sell_product),
    path('addExpenses', add_expenses),
    path('myProduction', my_production),
    path('myStock', my_stock),
    path('mySales', my_sales),
    path('myExpenses', my_expenses),
    path('test/', test),
    path('test/result/', result),
    path('imagetest', image_test),
    path('npktest',npk_test),
    
]