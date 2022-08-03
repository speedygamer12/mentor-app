from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views import (registration_view,login_view, VerifyEmail,
                                    LogoutAPIView, RequestPasswordResetEmail, 
                                    RequestPasswordResetEmail, PasswordTokenCheckAPI, 
                                    SetNewPasswordAPIView)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', registration_view, name='register'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')
]