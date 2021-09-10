from django.urls import path
from .views import *

urlpatterns = [
    path('', index),

    # path('viewProducts', view_products),
    # path('viewProducts/editComment', edit_comment),
    # path('viewProducts/delete/comment/<int:id>', delete_comment),
    # path('viewProducts/report', report_product),
    path('allProducts/', all_products),
    path('productdetails/<int:prod_id>', product_details),
    path('buy_product/<int:prod_id>', buy_product_request),

    path('prodBuyRequests', product_bought_requests),
    path('prodBuyRequests/<str:action>', product_bought_requests),
    path('approvedProducts', approved_prod_requests),

    path('editProdRequest/<int:req_id>', edit_prod_buy_requests),
    path('deleteProdRequest/<int:req_id>', delete_prod_buy_requests),

    path('allEquipments/', all_equipments),
    path('equipmentdetails/<int:eqp_id>', equipment_details),
    path('purchase/<int:eqp_id>', purchase_request),
    path('rent/<int:eqp_id>', rent_request),

    path('reportEqp/<int:eqp_id>', report_eqp_view),
    path('reportProd/<int:prod_id>', report_prod_view),

    path('eqpBuyRequests', equipment_bought_requests),
    path('eqpBuyRequests/<str:action>', equipment_bought_requests),
    
    path('eqpRentRequests', equipment_rented_requests),
    path('eqpRentRequests/<str:action>', equipment_rented_requests),
    path('equipments/<str:action>', approved_eqp_requests),

    path('editBuyRequest/<int:req_id>', edit_eqp_buy_requests),
    path('deleteBuyRequest/<int:req_id>', delete_eqp_buy_requests),

    path('editRentRequest/<int:req_id>', edit_eqp_rent_requests),
    path('deleteRentRequest/<int:req_id>', delete_eqp_rent_requests),

    path('profile/<int:user_id>', profile),
    path('profile/<int:user_id>/edit', edit_profile),

    path('changePassword/', change_password),
    path('feedback/', feedback),

    path('view-ticket/', view_ticket),

    path('sortproduct/', sort_product),
    path('searchproduct/', search_product),


    # path('viewEquipments/editComment', edit_eqp_comment),
    # path('viewEquipments/delete/comment/<int:id>', delete_eqp_comment),
    # path('viewEquipments/report', report_equipment),

    path('reportForm', report_form),
    
]