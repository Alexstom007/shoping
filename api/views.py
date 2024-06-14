from django.shortcuts import get_object_or_404
from django.db.models import Sum, F

from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Category, Product, Cart, CartProduct
from .serializers import (CategorySerializer,
                          ProductSerializer,
                          CartSerializer,
                          CartProductSerializer)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_or_create_cart(self, user):
        return Cart.objects.get_or_create(user=user)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def modify_product(self, request):
        product_id = request.data.get('product_id')
        action_type = request.data.get('action')
        product = get_object_or_404(Product, id=product_id)
        cart, _ = self.get_or_create_cart(request.user)
        
        if action_type == 'add':
            cart.products.add(product)
            message = 'product added'
        elif action_type == 'remove':
            cart.products.remove(product)
            message = 'product removed'
        else:
            message = 'action performed'
        
        cart.save()
        return Response({'status': message}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_quantity(self, request, pk=None):
        cart_product = get_object_or_404(CartProduct, cart__user=request.user, pk=pk)
        quantity = request.data.get('quantity', 1)
        cart_product.quantity = quantity
        cart_product.save()
        return Response({'status': 'quantity updated'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def retrieve_cart(self, request):
        cart, _ = self.get_or_create_cart(request.user)
        cart_products = CartProduct.objects.filter(cart=cart)
        cart_products_serializer = CartProductSerializer(cart_products, many=True)
        cart_data = cart_products.aggregate(
            total_quantity=Sum('quantity'),
            total_cost=Sum(F('quantity') * F('product__price'))
        )
        return Response({
            'products': cart_products_serializer.data,
            'total_quantity': cart_data['total_quantity'] or 0,
            'total_cost': cart_data['total_cost'] or 0
        })


class StandardResultsSetPagination(PageNumberPagination):
    """Пагинация"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Список категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Список товаров."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
