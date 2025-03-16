from django.core.cache import cache
from rest_framework import serializers

from app_users.models import User


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone","password")

class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','full_name','phone')

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match")
        return data

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, data):
        phone = data.get('phone')
        otp = data.get('otp')
        cached_data = cache.get(phone)
        if not cached_data or str(cached_data) != otp:
            raise serializers.ValidationError("Noto‘g‘ri yoki eskirgan OTP")
        return data

class SetNewPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Parollar mos kelmadi")
        return data