from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from app1.models import User
from .models import *
from .tasks import *


class ReservationsSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['user', 'contact', 'date']
        extra_kwargs = {
            'user': {'read_only': True},}

    def create(self, validated_data):
        if Reservation.objects.filter(user=self.context['request'].user, is_canceled=False, is_doing=False).exists():
            raise serializers.ValidationError('reservation already exists')
        else:
            validated_data['user'] = self.context.get('request').user
            return create_reserve.apply_async(kwargs=validated_data).get()


class ReservationsForAdminSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['user', 'date', 'contact', 'is_canceled', 'is_doing']
