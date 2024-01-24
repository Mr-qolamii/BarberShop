from rest_framework.serializers import ModelSerializer

from .models import *


class ReservationsSerializer(ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['content', 'date']

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(**validated_data)

