from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from .tasks import *


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'tell', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {
                'style':
                    {'input_type': 'password'},
                'write_only': True
            },
            'tell': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('passwords do not match')
        attrs.pop('password_confirm', None)
        return attrs

    def create(self, validated_data):
        return create_user.apply_async(kwargs=validated_data).get()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'profile_pic', 'firstname', 'lastname', 'age']
        extra_kwargs = {'user': {"read_only": True}, 'profile_pic': {"required": False},
                        'firstname': {"required": False},
                        'lastname': {"required": False}, 'age': {"required": False}}


class UserSetPasswordSerializer(serializers.Serializer):
    password_old = serializers.CharField()
    password_now = serializers.CharField(style={'input_type': 'password'})
    password_confirm = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs['password_now'] != attrs['password_confirm']:
            raise serializers.ValidationError('passwords do not match')
        return attrs


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


class ResetPasswordSerializer(serializers.Serializer):
    username_now = serializers.CharField()
    password_confirm = serializers.CharField()

    def validate(self, attrs):
        if attrs['password_now'] != attrs['password_confirm']:
            raise serializers.ValidationError('passwords do not match')
        return attrs


class SendSMSForResetPasswordSerializer(serializers.Serializer):
    tell = PhoneNumberField()

    def validate(self, attrs):
        if User.objects.get(tell=attrs["tell"]).exist():
            return attrs
        else:
            raise serializers.ValidationError('tel not exist')
