from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('addProductsForSale', products_for_sale),

    # path('myProducts', my_products),
    # path('myProducts/edit/<int:id>', edit_products),
    # path('myProducts/delete/<int:id>', delete_product),
    # path('myProducts/editComment', edit_comment),
    # path('myProducts/delete/comment/<int:id>', delete_comment),

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
    path('imagetest', image_test),
    path('detailReport', profit_loss_report),

    # path('generalTable', general_table),
    # path('detailsTable', details_table),

    path('profile', profile),
    path('editProfile', edit_profile),

    # path('test/result/', result),
    path('npktest',npk_result),

    path('buyequipment/', farmerstovenders),
    path('myproducts/', my_products),
    path('equipmentdetails/', equipment_Details),
    path('editproduct/', edit_product)
    
]