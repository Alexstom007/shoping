from rest_framework import serializers
from .models import Cart, CartProduct, Category, Subcategory, Product


class CartProductSerializer(serializers.ModelSerializer):
    """Добавление товара в связную модель."""
    class Meta:
        model = CartProduct
        fields = ['product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    """Чтение модели корзина."""
    products = CartProductSerializer(many=True, source='cartproduct_set')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'products', 'created_at', 'updated_at']


class SubcategorySerializer(serializers.ModelSerializer):
    """Чтение модели cубкатегория."""
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'slug', 'image']


class CategorySerializer(serializers.ModelSerializer):
    """Чтение модели категория."""
    subcategories = SubcategorySerializer(source='subcategory_set', many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'subcategories']


class ProductSerializer(serializers.ModelSerializer):
    """Чтение модели продукт."""
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'image_small', 'image_medium', 'image_large', 'subcategory']
