from rest_framework.mixins import *
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
from .models import Category,Brand,Product
from .serializers import *
from rest_framework import viewsets
from django.db.models import Prefetch
class GeneralMixin(GenericViewSet,ListModelMixin,RetrieveModelMixin):
    pass

class ProductViewSet(GeneralMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Product.objects.select_related('brand__city').prefetch_related('images')\
        .prefetch_related(
            Prefetch('favorites_product', queryset=Favorite.objects.filter(user=user), to_attr='user_favorites')
        ).all()
        
        is_active = self.request.query_params.get('active', 'true').lower() == 'true'
        city = self.request.query_params.get('city') 
        if city: 
            queryset = queryset.filter(brand__city__name_en=city)
            
        queryset = queryset.filter(is_active=is_active)

        return queryset
    
class CategoryViewSet(GeneralMixin):

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset

    serializer_class = CategorySerializer

class ProductCategoryViewSet(GeneralMixin):
    serializer_class = ProductListFromCategorySerializer
    

    def get_queryset(self):
        queryset = ProductCategory.objects.prefetch_related('product__images','product__brand','category').all()
        category_pk = self.kwargs.get('category_pk')

        return queryset.filter(category_id = category_pk)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)

        product_list = [item['product'] for item in serializer.data]
        print(queryset)
        return Response(product_list)
    
    def retrieve(self, request, category_pk=None, pk=None):
        if not category_pk or not pk:
            return Response({"error": "Both Category ID and Product ID are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_category = ProductCategory.objects.get(category_id=category_pk, product_id=pk)
        except ProductCategory.DoesNotExist:
            return Response({"error": "Product not found in this category."}, status=status.HTTP_404_NOT_FOUND)
        # print(product_category.product)
        serializer = ProductSerializer(product_category.product)
        return Response(serializer.data)
    

class FavoriteView(GeneralMixin,CreateModelMixin,DestroyModelMixin):
    def get_queryset(self):
        return Favorite.objects.select_related('product__brand','user').prefetch_related('product__images')\
                               .filter(user_id= self.request.user.id)
    serializer_class = FavoriteSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}
    
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
        return Order.objects.prefetch_related('items__product__images')\
                            .prefetch_related('items__product__brand__city')\
                            .select_related('user')
    serializer_class = OrderSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}



