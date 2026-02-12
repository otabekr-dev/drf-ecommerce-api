from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('Stock manfiy raqamlarda bulmaydi') 
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Narx xato kiritildi, iltimos manfiy son kiritmang')
        return value
       