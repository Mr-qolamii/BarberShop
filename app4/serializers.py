from rest_framework import serializers

from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all_'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['product', 'user', 'date']
        extera_kwargs = {'date': {"read_only": True}, }


class SoldOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
