from django.urls import path, include
from .views import *

urlpatterns = [
    path('users/', UserAPIView.as_view()),
    path('users/<str:username>', UserDetail.as_view()),
    path('users/id/<int:id>', UserById.as_view()),
    path('users/id/<int:user_id>/details', GetUserDetails.as_view()),

    path('reportuser/', ReportUserView.as_view()),

    path('profile/', CreateProfile.as_view()),
    path('profile/<int:user_id>', GetProfileType.as_view()),
    path('profile/<int:user_id>/edit', UpdateProfileView.as_view()),

    # products
    # path('products/', ProductsAPIView.as_view()),
    # path('products/<int:id>', ProductDetails.as_view()),

    path('productsOnSale/', ProductsForSaleView.as_view()),
    path('productsOnSale/<int:id>', ProductsForSaleDetails.as_view()),
    path('productsOnSale/mine/<int:user_id>', MyProductsOnSale.as_view()),

    path('products/production/', ProductionAPIView.as_view()),
    path('products/production/<int:id>', ProductionDetails.as_view()),
    path('products/production/mine/<int:user_id>', MyProductions.as_view()),

    path('products/stock/', ProductStockAPIView.as_view()),
    path('products/stock/mine/<int:user_id>', MyProductStock.as_view()),

    path('notes/', NoteAPIView.as_view()),
    path('notes/<int:id>', NoteDetails.as_view()),

    path('productsOnSale/comments', ProductCommentView.as_view()),
    path('productsOnSale/comments/<int:com_id>', CommentDetails.as_view()),

    path('productsOnSale/reports', ProductReportView.as_view()),
    path('productsOnSale/reports/<int:id>', ReportDetails.as_view()),
    
    # path('sellProducts/', ProductSoldView.as_view()),
    # path('sellProducts/<int:id>', ProductSoldDetails.as_view()),
    # path('sellProducts/seller/<int:id>', SellerSalesDetails.as_view()),
    # path('sellProducts/buyer/<int:id>', BuyerSalesDetails.as_view()),

    path('expenses/', ExpenseAPIView.as_view()),
    path('expenses/<int:id>', ExpenseDetails.as_view()),
    path('expenses/user/<int:user_id>', MyExpenses.as_view()),

    path('homeExpenses/', HomeExpenseAPIView.as_view()),
    path('homeExpenses/<int:id>', HomeExpenseDetails.as_view()),
    path('homeExpenses/user/<int:user_id>', MyHomeExpense.as_view()),

    # equipments
    # path('equipment/', EquipmentAPIView.as_view()),
    # path('equipment/<int:id>', EquipmentDetails.as_view()),
    
    path('equipmentToDisplay/', EquipmentsToDisplayView.as_view()),
    path('equipmentToDisplay/<int:id>', EquipmentsToDisplayDetails.as_view()),
    path('equipmentToDisplay/mine/<int:user_id>', MyEquipments.as_view()),

    path('equipmentToDisplay/reports', EquipmentReportView.as_view()),
    path('equipmentToDisplay/reports/<int:id>', EqpReportDetails.as_view()),

    path('equipmentToDisplay/comments', EquipmentCommentView.as_view()),
    path('equipmentToDisplay/comments/<int:com_id>', EqpCommentDetails.as_view()),

    path('equipmentToDisplay/buy', BuyEquipmentView.as_view()),
    path('equipmentToDisplay/buy/<int:id>', BuyEquipmentDetails.as_view()),
    path('equipmentToDisplay/buy/buyer/<int:id>', BoughtEquipmentsBuyer.as_view()),
    path('equipmentToDisplay/buy/seller/<int:id>', SoldEquipmentSeller.as_view()),

    path('equipmentToDisplay/rent', RentEquipmentView.as_view()),
    path('equipmentToDisplay/rent/<int:id>', RentEquipmentDetails.as_view()),
    path('equipmentToDisplay/rent/buyer/<int:id>', RentedEquipmentsBuyer.as_view()),
    path('equipmentToDisplay/rent/seller/<int:id>', RentedEquipmentSeller.as_view()),

    path('profitloss/<int:id>', ProfitLossReportView.as_view()),

    path('buyProduct/', BuyProductRequest.as_view()),
    path('editBuyRequest/<int:id>', ProductRequestDetails.as_view()),
    path('myRequests/buyers/<int:id>', BuyersProductRequests.as_view()),
    path('productRequests/<int:id>', FarmerProductRequests.as_view()),

    path('changeRequestStatus/<int:id>', ChangeProductRequestStatus.as_view()),

    path('changeEqpBuyStatus/<int:id>', ChangeEqpBuyRequestStatus.as_view()),
    path('changeEqpRentStatus/<int:id>', ChangeEqpRentRequestStatus.as_view()),

    path('npktest', NPKTestView.as_view()),
    path('imagetest', ImageTestView.as_view()),

]
