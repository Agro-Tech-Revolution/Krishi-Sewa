from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard),
    path('addProducts', add_products),
    path('admin', test),
    path('addEquipments', add_equipments),
    path('users/', users),
    path('reportUser/', report_user),
    path('reportEquip/', report_equipment),
    path('reportProduct/', report_product),
    path('farmers/', famers),
    path('buyers/', buyers),
    path('vendors/', vendors),
    path('farmer-list', farmer_list),
    path('vendors-list', vendors_list),
    path('buyers-list', buyers_list)

]