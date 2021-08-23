from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard),
    path('addProducts/', add_products),
    path('editProducts/<int:prod_id>', edit_product_details),
    path('deleteProducts/<int:prod_id>', delete_product),

    path('admin', test),

    path('addEquipments/', add_equipments),
    path('editEquipments/<int:eqp_id>', edit_equipment_details),
    path('deleteEquipments/<int:eqp_id>', delete_equipment),
    
    path('users/', users),
    path('disableUser/<int:user_id>', disable_user_account),
    path('activateUser/<int:user_id>', activate_user_account),

    path('reportUser/', report_user),
    path('reportEquip/', report_equipment),
    path('reportProduct/', report_product),
    path('farmers/', famers),
    path('buyers/', buyers),
    path('vendors/', vendors),
    path('farmers-list', farmer_list),
    path('vendors-list', vendors_list),
    path('buyers-list', buyers_list)

]