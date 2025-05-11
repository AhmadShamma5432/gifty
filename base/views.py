from rest_framework.mixins import *
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
from .models import Category,Brand,Product
from .serializers import *
from django.db.models import Q
from rest_framework import viewsets
from django.db.models import Prefetch,Count
class GeneralMixin(GenericViewSet,ListModelMixin,RetrieveModelMixin):
    pass

class ProductViewSet(GeneralMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        ordering = self.request.query_params.get('ordering')
        queryset = Product.objects\
        .select_related('brand__city').prefetch_related('images')\
        .prefetch_related(
            Prefetch('favorites_product', queryset=Favorite.objects.filter(user=user), to_attr='user_favorites')
        )
        if ordering == 'most_ordered':
            queryset = queryset.annotate(ordering_count =Count('orderd_products')).order_by('-ordering_count')
        elif ordering == 'most_favorited':
            queryset = queryset.annotate(favorites_count=Count('favorites_product')).order_by('-favorites_count')
        elif ordering == 'last_added':
            queryset = queryset.order_by('-date_of_creation')

        is_active = self.request.query_params.get('active', 'true').lower() == 'true'
        city = self.request.query_params.get('city') 
        if city: 
            queryset = queryset.filter(brand__city__name_en=city)
            
        queryset = queryset.filter(is_active=is_active)

    
        return queryset
    def get_serializer_context(self):
        return {'request': self.request}
    
class CategoryViewSet(GeneralMixin):

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset

    serializer_class = CategorySerializer

class FavoriteView(GeneralMixin,CreateModelMixin,DestroyModelMixin):
    def get_queryset(self):
        return Favorite.objects.select_related('product__brand','user').prefetch_related('product__images')\
                               .filter(user_id= self.request.user.id)
                               
    serializer_class = FavoriteSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id,
                "request": self.request}
    
class CityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cities to be viewed or edited.
    """
    queryset = City.objects.all()  # Order by English name
    serializer_class = CitySerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cities to be viewed or edited.
    """
    def get_queryset(self):
        favorite_prefetch = Prefetch(
            'items__product__favorites_product',
            queryset=Favorite.objects.filter(user=self.request.user),
            to_attr='user_favorites'
        )
        return Order.objects.prefetch_related('items__product__images')\
                            .prefetch_related('items__product__brand__city')\
                            .prefetch_related(favorite_prefetch)\
                            .select_related('user')

    def get_serializer_context(self):
        return {"user_id": self.request.user.id,
                "user": self.request.user,
                "request":self.request}
    
    def get_serializer_class(self):
        return OrderSerializer
        # if self.request.method in ['PATCH','PUT']:
        #     return UpdateOrderSerializer


class CouponViewSet(viewsets.ModelViewSet):
    serializer_class = CouponSerializer
    def get_queryset(self):
        code = self.request.query_params.get('code', None)
        queryset = Coupon.objects.get(code__exact=code)
        return [queryset]