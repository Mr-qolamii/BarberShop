from rest_framework import serializers

from .models import *
from .tasks import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['pk', 'product', 'user', 'count', 'date', 'is_done']
        extra_kwargs = {'pk': {'read_only': True}, 'user': {'read_only': True}, 'product': {'read_only': True},
                        'date': {'read_only': True}, 'is_done': {'read_only': True}}

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        attrs['product_id'] = self.context['request'].parser_context['kwargs']['pk']
        if Order.objects.filter(user=attrs['user'], product=attrs['product']).exists() and self.context[
            'request'].method == 'POST':
            raise serializers.ValidationError("This product is in your shopping cart")
        return attrs

    def create(self, validated_data):
        return create_order.apply_async(kwargs=validated_data).get()


class SoldOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
