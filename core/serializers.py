from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Debugging statement to check the contents of attrs
        # print(f"Attributes received: {attrs}")

        credentials = {
            'phone': attrs.get('phone'),
            'password': attrs.get('password')
        }

        if not credentials['phone']:
            raise serializers.ValidationError('phone is required')
        if not credentials['password']:
            raise serializers.ValidationError('Password is required')

        user = User.objects.filter(phone=credentials['phone']).first()
        if user:
            if user.check_password(credentials['password']):
                # Use the phone as the username field for token generation
                data = super().validate({
                    'phone': user.phone,  # Use 'username' key here
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
        fields = ['id','name','email','phone','password']

class UserSerializer(BaseUserSerializer):
    # first_name = serializers.CharField(required=True)
    class Meta(BaseUserSerializer.Meta):
        #the id is auto_field so it doesn't shown in the view of creation
        fields = ['id','name','email','phone']



class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','phone']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','phone']

