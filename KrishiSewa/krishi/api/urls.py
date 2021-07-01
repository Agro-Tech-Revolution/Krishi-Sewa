from django.urls import path, include
from .views import *

urlpatterns = [
    path('users/', UserAPIView.as_view()),
    path('users/<str:username>', UserDetail.as_view()),
    path('users/id/<int:id>', UserById.as_view()),

    path('profile/', CreateProfile.as_view()),
    path('profile/<int:user_id>', GetProfileType.as_view()),

    path('notes/', NoteAPIView.as_view()),
    path('notes/<int:id>', NoteDetails.as_view()),

    path('products/', ProductAPIView.as_view()),
    path('products/mine/<int:user_id>', MyProducts.as_view()),
    path('products/<int:prod_id>', ProductDetails.as_view()),

    path('products/comments', ProductCommentView.as_view()),
    path('products/comments/<int:com_id>', CommentDetails.as_view()),
    path('products/<int:prod_id>/comments', CommentOfProduct.as_view()),
    path('products/comments/user/<int:user_id>', CommentsOnMyProduct.as_view()),

    path('products/reports', ProductReportView.as_view()),
    path('products/reports/<int:id>', ReportDetails.as_view()),
    path('products/<int:id>/reports', ReportsOnProduct.as_view()),
    path('products/reports/users/<int:user_id>', ProductReportByUser.as_view()),
    
    path('equipment/', CreateEquipment.as_view()),
    path('equipment/<int:id>', EquipmentDetails.as_view())
]
