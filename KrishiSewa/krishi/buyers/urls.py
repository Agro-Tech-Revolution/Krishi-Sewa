from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('viewProducts', view_products),
    path('viewProducts/editComment', edit_comment),
    path('viewProducts/delete/comment/<int:id>', delete_comment),
    path('viewProducts/report', report_product),

    
]