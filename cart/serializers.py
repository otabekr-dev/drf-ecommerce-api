from rest_framework import serializers
from .models import CartItem

class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='products.name')
    product_price = serializers.ReadOnlyField(source='products.price')
    total = serializers.ReadOnlyField()
    

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'total']

        
