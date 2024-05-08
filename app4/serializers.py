from rest_framework import serializers

from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['product', 'user', 'count', 'date']
        extra_kwargs = {'user': {'read_only': True}, 'product': {'read_only': True}, 'date': {'read_only': True}}

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        attrs['product'] = Product.objects.get(pk=self.context['request'].parser_context['kwargs']['pk'])
        if Order.objects.filter(user=attrs['user'], product=attrs['product']).exists():
            raise serializers.ValidationError("This product is in your shopping cart")
        return attrs


class SoldOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
