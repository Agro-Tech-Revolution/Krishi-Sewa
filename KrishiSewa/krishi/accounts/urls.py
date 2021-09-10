from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home),
    path('login/', login_view),
    path('register', register_view),
    path('history', history),
    path('feedback', feedback),
    path('logout', logout_user),
    path('reportuser/<int:user_id>/', report_user),
    path('send-response/<int:ticket_id>/', send_response),
    path('changePassword/', change_password),

    path('submit-feedback/', submit_feedback),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_change.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),
]

