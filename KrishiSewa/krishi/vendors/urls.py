from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('addEquipments', equipments),
    path('myEquipments', my_equipments),
    path('myEquipments/edit/<int:id>', edit_equipment),
    path('myEquipments/delete/<int:id>', delete_equipment),
    path('myEquipments/editComment', edit_comment),
    path('myEquipments/delete/comment/<int:id>', delete_comment),
    
]