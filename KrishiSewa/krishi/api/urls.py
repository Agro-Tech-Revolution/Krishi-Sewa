from django.urls import path, include
from .views import *

urlpatterns = [
    path('users/', UserAPIView.as_view()),
    path('users/<str:username>', UserDetail.as_view()),
    path('users/id/<int:id>', UserById.as_view()),

    path('profile/', CreateProfile.as_view()),
    path('profile/<int:user_id>', GetProfileType.as_view()),

    # new additions
    path('products/', ProductsAPIView.as_view()),
    path('products/<int:id>', ProductDetails.as_view()),

    path('productsOnSale/', ProductsForSaleView.as_view()),
    path('productsOnSale/<int:id>', ProductsForSaleDetails.as_view()),
    path('productsOnSale/mine/<int:user_id>', MyProductsOnSale.as_view()),

    path('products/production/', ProductionAPIView.as_view()),
    path('products/production/<int:id>', ProductionDetails.as_view()),
    path('products/production/mine/<int:user_id>', MyProductions.as_view()),

    path('products/stock/', ProductStockAPIView.as_view()),
    path('products/stock/mine/<int:user_id>', MyProductStock.as_view()),
    # end

    # path('notes/', NoteAPIView.as_view()),
    # path('notes/<int:id>', NoteDetails.as_view()),

    path('productsOnSale/comments', ProductCommentView.as_view()),
    path('productsOnSale/comments/<int:com_id>', CommentDetails.as_view()),

    path('productsOnSale/reports', ProductReportView.as_view()),
    path('productsOnSale/reports/<int:id>', ReportDetails.as_view()),
    
    path('sellProducts/', ProductSoldView.as_view()),
    path('sellProducts/<int:id>', ProductSoldDetails.as_view()),
    path('sellProducts/seller/<int:id>', SellerSalesDetails.as_view()),
    path('sellProducts/buyer/<int:id>', BuyerSalesDetails.as_view()),

    path('equipment/', CreateEquipment.as_view()),
    path('equipment/mine/<int:user_id>', MyEquipments.as_view()),
    path('equipment/<int:id>', EquipmentDetails.as_view()),

    path('equipment/comments', EquipmentCommentView.as_view()),
    path('equipment/comments/<int:com_id>', EqpCommentDetails.as_view()),
    path('equipment/<int:eqp_id>/comments', CommentOfEquipment.as_view()),
    path('equipment/comments/user/<int:user_id>', CommentsOnMyEquipment.as_view()),

    path('equipment/reports', EquipmentReportView.as_view()),
    path('equipment/reports/<int:id>', EqpReportDetails.as_view()),
    path('equipment/<int:id>/reports', ReportsOnEquipment.as_view()),
    path('equipment/reports/users/<int:user_id>', EquipmentReportByUser.as_view()),
]
