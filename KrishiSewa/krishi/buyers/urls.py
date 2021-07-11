from django.urls import path
from .views import *

urlpatterns = [
    path('', index),

    path('viewProducts', view_products),
    path('viewProducts/editComment', edit_comment),
    path('viewProducts/delete/comment/<int:id>', delete_comment),
    path('viewProducts/report', report_product),

    path('viewEquipments', view_equipments),
    path('viewEquipments/editComment', edit_eqp_comment),
    path('viewEquipments/delete/comment/<int:id>', delete_eqp_comment),
    path('viewEquipments/report', report_equipment),

    path('reportForm', report_form),
    
]