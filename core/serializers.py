from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Debugging statement to check the contents of attrs
        # print(f"Attributes received: {attrs}")

        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        if not credentials['email']:
            raise serializers.ValidationError('Email is required')
        if not credentials['password']:
            raise serializers.ValidationError('Password is required')

        user = User.objects.filter(email=credentials['email']).first()
        if user:
            if user.check_password(credentials['password']):
                # Use the email as the username field for token generation
                data = super().validate({
                    'email': user.email,  # Use 'username' key here
                    'password': credentials['password']
                })
                return data
            else:
                raise serializers.ValidationError('Invalid password')
        else:
            raise serializers.ValidationError('User not found')   
              
class UserCreateSerializer(BaseUserCreateSerializer):
    # first_name = serializers.CharField(required=True)
    class Meta(BaseUserCreateSerializer.Meta):
        #the id is auto_field so it doesn't shown in the view of creation
        fields = ['id','name','email','phone_number','address','password']

class UserSerializer(BaseUserSerializer):
    # first_name = serializers.CharField(required=True)
    class Meta(BaseUserSerializer.Meta):
        #the id is auto_field so it doesn't shown in the view of creation
        fields = ['id','name','email','phone_number','address']



class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','phone_number','address']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','phone_number','address']

