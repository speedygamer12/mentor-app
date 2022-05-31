from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import status, viewsets
# from rest_framework_simplejwt.tokens import RefreshToken

from user_app import models
from user_app.api.serializers import RegistrationSerializer


@api_view(['POST',])
def logout_view(request):
    
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status.HTTP_200_OK) 

@api_view(['POST',])
def registration_view(request):
    
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            # print(account.username, account.email)

            data['response'] = "Registration Successfull"
            data['username'] = account.username
            data['email'] = account.email
            data['dsnid'] = account.dsnid
            data['user_type'] = account.user_type
            
            token = Token.objects.get(user=account).key   #getting a token from our db  
            data['token'] = token #passing the token as part of the response
            
            # refresh = RefreshToken.for_user(account)
            # data['token'] = {
            #     'refresh': str(refresh),
            #     'access': str(refresh.access_token),
            # }
            
        else:
            data = serializer.errors
            
        return Response(data, status=status.HTTP_201_CREATED) 

