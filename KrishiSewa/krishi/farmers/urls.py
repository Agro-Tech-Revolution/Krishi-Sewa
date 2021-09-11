from django.urls import path
from .views import *

urlpatterns = [
    path('', index),

    path('feedback', feedback),
    # path('addProductsForSale', products_for_sale),


    path('addProduction', add_production),
    path('editProduction/<int:id>', edit_production),
    path('deleteProduction/<int:id>', delete_production),

    # path('myProducts/sell/<int:id>', sell_product),

    path('mySales', my_sales),
    # path('editSales/<int:id>', edit_sales),
    # path('deleteSales/<int:id>', delete_sales),

    path('addHomeExpenses', add_home_expenses),
    path('myHomeExpenses', my_home_expenses),
    path('editHomeExpense/<int:exp_id>', edit_home_expense),
    path('deleteHomeExpense/<int:exp_id>', delete_home_expense),
    
    path('myProduction', my_production),
    path('myStock', my_stock),

    path('addExpenses', add_expenses),
    path('myExpenses', my_expenses),
    path('editExpense/<int:exp_id>', edit_my_expense),
    path('deleteExpense/<int:exp_id>', delete_my_expense),


    path('imagetest', image_test),
    path('npk-records', npk_records),
    path('img-test-records', image_test_records),
    path('detailReport', profit_loss_report),

    # path('generalTable', general_table),
    # path('detailsTable', details_table),

    path('profile/<int:user_id>', profile),
    path('profile/<int:user_id>/edit', edit_profile),

    path('changePassword/', change_password),

    path('npktest', npk_result),

    path('allEquipments/', all_equipments),
    path('equipmentdetails/<int:eqp_id>', equipment_details),
    path('purchase/<int:eqp_id>', purchase_request),
    path('rent/<int:eqp_id>', rent_request),

    path('reportEqp/<int:eqp_id>', report_eqp_view),

    path('addproduct/', add_product),
    path('myproducts/', my_products),
    path('editproduct/<int:prod_id>', edit_product),
    path('deleteproduct/<int:prod_id>', delete_product),
    path('myproducts/<int:prod_id>', product_details),
    
    path('productRequests', product_requests),
    path('productRequests/<str:action>', product_requests),
    path('approveRequest/<int:prod_req_id>', approve_product_request),
    path('disapproveRequest/<int:prod_req_id>', disapprove_product_request),

    path('eqpBuyRequests', equipment_bought_requests),
    path('eqpBuyRequests/<str:action>', equipment_bought_requests),
    path('equipments/<str:action>', approved_eqp_requests),

    path('eqpRentRequests', equipment_rented_requests),
    path('eqpRentRequests/<str:action>', equipment_rented_requests),
    
    path('editBuyRequest/<int:req_id>', edit_eqp_buy_requests),
    path('deleteBuyRequest/<int:req_id>', delete_eqp_buy_requests),

    path('editRentRequest/<int:req_id>', edit_eqp_rent_requests),
    path('deleteRentRequest/<int:req_id>', delete_eqp_rent_requests),

    path('view-ticket/', view_ticket),

]
