from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.mixins import * 
from rest_framework.viewsets import GenericViewSet
from .models import User
from .serializers import UserRetrieveSerializer,UserUpdateSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserUpdateView(RetrieveModelMixin,UpdateModelMixin,ListModelMixin,GenericViewSet):

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UserUpdateSerializer
        else:
            return UserRetrieveSerializer