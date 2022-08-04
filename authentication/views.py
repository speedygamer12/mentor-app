from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, views, generics, viewsets
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponsePermanentRedirect
from django.template.loader import get_template
from django.template import Context

import jwt
import environ

from . import signals
from .serializers import (RegistrationSerializer, EmailVerificationSerializer, 
                            LogoutSerializer, SetNewPasswordSerializer, LoginSerializer,
                            RequestPasswordResetEmailSerializer)
from .utils import Util


env = environ.Env()
environ.Env.read_env()

User = get_user_model()
from django.urls import reverse

class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [env('APP_SCHEME'), 'http', 'https']


# @api_view(['POST',])
# def logout_view(request):
    
#     if request.method == 'POST':
#         request.user.auth_token.delete()
#         return Response(status.HTTP_200_OK) 

@api_view(['POST',])
def registration_view(request):
    
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)        
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            
            user = User.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token

            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            context = Context({'url': absurl, 'name': user.username})

            html_content, text_content = get_template('register-mail.html').template, get_template('register-mail.txt').template
            data = {'html_content': html_content, 'text_content': text_content, 'to_email': user.email, 
                    'email_subject': 'Verify your email', 'context': context}

            Util.send_email(data) 

        else:
            user_data = serializer.errors  
            
        return Response(user_data, status=status.HTTP_201_CREATED)

# @api_view(['POST',])
# def resend_verification(request):

#     if request.method == 'POST':
#         serializer = ResendVerificationSerializer
#         if serializer.is_valid():
#             email = request.data.get('email', '')
#             if User.objects.filter(email=email).exists():
#                 user = User.objects.get(email=email)
#                 if not user.is_verified:
#                     user.is_verified = True
#                     user.save()
#                 return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
#                 except jwt.ExpiredSignatureError as identifier:
#             return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
#             except jwt.exceptions.DecodeError as identifier:
#                 return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(views.APIView):

    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
def login_view(request):
    
    if request.method == 'POST':
        print("request checked")
        print(request.data)
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.data
        else:
            user_data = serializer.errors  
        return Response(user_data, status=status.HTTP_200_OK)

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            finalurl = absurl+"?redirect_url="+redirect_url

            html_content, text_content = get_template('reset-password.html').template, get_template('reset-password.html').template
            
            context = Context({'url': finalurl, 'email': user.email})
            data = {'html_content': html_content, 'text_content': text_content, 'to_email': user.email,
                    'email_subject': 'Reset your passsword', 'context': context}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(env('FRONTEND_URL')+'?token_valid=False')
            else:
                if redirect_url and len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
                else:
                    # return CustomRedirect(env('FRONTEND_URL')+'?token_valid=False')
                    return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)