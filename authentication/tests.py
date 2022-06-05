from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.urls import reverse

from user_app import models

from django.contrib.auth import get_user_model
User=get_user_model()

class RegisterTestCase(APITestCase):
    
    def test_register(self):
        
        data = {
            'username': 'testcase',
            'dsnid': '12345678',
            'user_type': 1,
            'password': 'Example@123',
            'password1': 'Example@123'
        }
        
        response = self.client.post(reverse('register'), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
       
class LoginLogoutTestCase(APITestCase):
    
    #new account
    def setUp(self):
        self.user = User.objects.create_user(username="example", user_type=1, dsnid='12345678', 
                                            password="Password@123")
    
    # def test_login(self):
        
    #     data = {
    #         "username": "example",
    #         "password": "password@123"
    #     }
        
    #     response = self.client.post(reverse('login'), data)
        
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_logout(self):
        self.token = Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        response = self.client.post(reverse('logout'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
     