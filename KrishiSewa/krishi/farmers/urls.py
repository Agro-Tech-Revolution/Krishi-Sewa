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
    
    path('myProducts/sell/<int:id>', sell_product),
    path('mySales', my_sales),
    path('editSales/<int:id>', edit_sales),
    path('deleteSales/<int:id>', delete_sales),

    path('addExpenses', add_expenses),
    path('myProduction', my_production),
    path('myStock', my_stock),
    
    path('myExpenses', my_expenses),

    # path('test/result/', result),

    path('imagetest', image_test),
    path('npktest',npk_result),


    path('imagetest/', image_test1),
    # path('imagetest_result/', get_image_model)
    # path('test_img', imageTest),

    
]