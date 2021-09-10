from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('addEquipments', equipments),
    path('myEquipments', my_equipments),
    path('myEquipments/<int:eqp_id>', equipment_details),
    path('editEquipment/<int:eqp_id>', edit_equipment),
    path('deleteEquipment/<int:eqp_id>', delete_equipment),
    path('myEquipments/editComment', edit_comment),
    path('myEquipments/delete/comment/<int:id>', delete_comment),

    path('profile/<int:user_id>', profile),
    path('profile/<int:user_id>/edit', edit_profile),

    path('changePassword/', change_password),

    path('feedback', feedback),
    # path('equipmentRequests', equipment_requests),
    # path('equipmentRequests/<str:action>', equipment_requests),

    path('eqpBuyRequests', equipment_bought_requests),
    path('eqpBuyRequests/<str:action>', equipment_bought_requests),
    # path('eqpuipments/<str:action>', approved_eqp_requests),

    path('eqpRentRequests', equipment_rented_requests),
    path('eqpRentRequests/<str:action>', equipment_rented_requests),
    # path('equipments/<str:action>', approved_eqp_requests),

    path('approveBuyRequest/<int:eqp_req_id>', approve_eqp_buy_request),
    path('disapproveBuyRequest/<int:eqp_req_id>', disapprove_eqp_buy_request),

    path('approveRentRequest/<int:eqp_req_id>', approve_eqp_rent_request),
    path('disapproveRentRequest/<int:eqp_req_id>', disapprove_eqp_rent_request),

    path('mysales', my_sales),
    path('mysales/<str:action>', my_sales),

    path('view-ticket/', view_ticket),
    
]