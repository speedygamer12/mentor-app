from rest_framework import serializers
from django.contrib.auth import get_user_model


User=get_user_model()
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'dsnid', 'user_type', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, attrs):
        # if attrs.get('dsn_id') != 'some validation criteria with regex':
        #     raise serial  izers.validation.ValidationError({'error: dsnID in correct'})

        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({'password':'password must match'})
        
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({'error':'Email already exists!'})
            
        return attrs

        
    def create(self, validated_data):
        
        password2 = validated_data.pop('password2')
        
        return  User.objects.create_user(**validated_data) 



