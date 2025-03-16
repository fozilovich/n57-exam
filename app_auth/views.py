from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from app_auth.serializers import (
    LoginSerializer, MeSerializer, ChangePasswordSerializer,
    VerifyOTPSerializer, SetNewPasswordSerializer
)
from app_users.models import User


class LoginAPIView(APIView): #Foydalanuvchini autentifikatsiya qilish (login)

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        phone = request.data.get("phone")
        password = request.data.get("password")

        user = User.objects.filter(phone=phone).first()

        # Agar foydalanuvchi mavjud bo‘lsa va paroli to‘g‘ri bo‘lsa
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)  # JWT token generatsiya qilinadi
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })

        return Response(
            {"status": False, "detail": "Telefon raqam yoki parol noto‘g‘ri"},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView): #Foydalanuvchini tizimdan chiqarish (logout)

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(RetrieveAPIView): #Hozirgi autentifikatsiya qilingan foydalanuvchi ma'lumotlarini olish

    serializer_class = MeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView): # Foydalanuvchi parolini yangilash

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user

            # Eski parol noto‘g‘ri bo‘lsa
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"status": False, "detail": "Your old password is incorrect"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Yangi parolni saqlash
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response(
                {"status": True, "detail": "Your password has been successfully updated!"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView): #SMS orqali yuborilgan OTP kodni tasdiqlash

    @swagger_auto_schema(request_body=VerifyOTPSerializer)
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']

            # Telefon raqamni kesh ga saqlash
            cache.set(f"verified_{phone}", True, timeout=900)

            return Response(
                {"status": True, "detail": "OTP verified successfully"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(APIView): #Parolni OTP tasdiqlangandan keyin yangilash

    @swagger_auto_schema(request_body=SetNewPasswordSerializer)
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            verified = cache.get(f"verified_{phone}")  # OTP tasdiqlanganmi tekshiramiz

            if not verified:
                return Response(
                    {"status": False, "detail": "OTP not verified"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.filter(phone=phone).first()
            if user:
                user.set_password(serializer.validated_data['new_password'])
                user.save()

                return Response(
                    {"status": True, "detail": "Password successfully set"},
                    status=status.HTTP_200_OK
                )

            return Response(
                {"status": False, "detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
