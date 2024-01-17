from rest_framework import serializers
from app1.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    password_2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'tell', 'password', 'password_2']
        extra_kwargs = {'password': {'style': {'input_type': 'password'}}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password_2']:
            raise serializers.ValidationError('passwords do not match')
        attrs.pop('password_2', None)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'profile_pic', 'firstname', 'lastname', 'age']
        extra_kwargs = {'user': {"read_only": True}}


class UserSetPasswordSerializer(serializers.ModelSerializer):
    password_now = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['password', 'password_now', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_2']:
            raise serializers.ValidationError('passwords do not match')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


class RestPasswordSerializer(serializers.Serializer):
    username_1 = serializers.CharField()
    password_2 = serializers.CharField()
