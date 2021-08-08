from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    # path('addProductsForSale', products_for_sale),

    # path('myProducts', my_products),
    # path('myProducts/edit/<int:id>', edit_products),
    # path('myProducts/delete/<int:id>', delete_product),
    # path('myProducts/editComment', edit_comment),
    # path('myProducts/delete/comment/<int:id>', delete_comment),

    path('addProduction', add_production),
    path('editProduction/<int:id>', edit_production),
    path('deleteProduction/<int:id>', delete_production),

    # path('myProducts/sell/<int:id>', sell_product),

    # path('mySales', my_sales),
    # path('editSales/<int:id>', edit_sales),
    # path('deleteSales/<int:id>', delete_sales),

    path('addHomeExpenses', add_home_expenses),
    
    path('myProduction', my_production),
    path('myStock', my_stock),

    path('addExpenses', add_expenses),
    path('myExpenses', my_expenses),
    path('editExpense/<int:exp_id>', edit_my_expense),
    path('deleteExpense/<int:exp_id>', delete_my_expense),


    path('imagetest', image_test),
    path('detailReport', profit_loss_report),

    # path('generalTable', general_table),
    # path('detailsTable', details_table),

    path('profile/<int:user_id>', profile),
    path('profile/<int:user_id>/edit', edit_profile),

    # path('test/result/', result),
    path('npktest', npk_result),

    path('allEquipments/', all_equipments),
    path('equipmentdetails/<int:eqp_id>', equipment_details),
    path('purchase/<int:eqp_id>', purchase_request),
    path('rent/<int:eqp_id>', rent_request),

    path('addproduct/', add_product),
    path('myproducts/', my_products),
    path('editproduct/<int:prod_id>', edit_product),
    path('deleteproduct/<int:prod_id>', delete_product),
    path('myproducts/<int:prod_id>', product_details),

]
