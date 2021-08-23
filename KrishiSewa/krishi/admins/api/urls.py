from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', DashboardView.as_view()),

    path('products/', ProductsAPIView.as_view()),
    path('products/<int:id>', ProductDetails.as_view()),

    path('equipment/', EquipmentAPIView.as_view()),
    path('equipment/<int:id>', EquipmentDetails.as_view()),

    path('allUsers/', AvailableUsersView.as_view()),
    path('userAction/<int:user_id>', ActionOnUserView.as_view()),

    path('farmers-list/', FarmersListView.as_view()),
    path('vendors-list/', VendorsListView.as_view()),
    path('buyers-list/', BuyersListView.as_view()),

    # path('vendors-sales', VendorEqpSalesView.as_view()),

]