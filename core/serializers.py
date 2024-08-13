from djoser.serializers import UserCreateSerializer as BaseUserCreateSerailizer, UserSerializer as BaseUserSerializer
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreateSerailizer):
    # first_name = serializers.CharField(required=True)
    class Meta(BaseUserCreateSerailizer.Meta):
        #the id is auto_field so it doesn't shown in the view of creation
        fields = ['id','email','username','password','first_name']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','username','email',]