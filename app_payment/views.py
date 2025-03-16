from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from app_common.paginations import Pagination
from app_common.permissions import AdminUser
from app_payment.models import Payment, Month, PaymentType
from app_payment.serializers import MonthSerializer, PaymentTypeSerializer, PaymentSerializer

class MonthViewSet(viewsets.ViewSet): #Oylarni boshqarish uchun API
    permission_classes = [AdminUser]

    def list(self, request): # Barcha oylarni olish
        months = Month.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(months, request)
        serializer = MonthSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):  # Bitta oy haqida ma'lumot olish
        month = get_object_or_404(Month, pk=pk)
        serializer = MonthSerializer(month)
        return Response(serializer.data)

    # Yangi oy yaratish
    @action(detail=False, methods=['post'], url_path='create/month')
    @swagger_auto_schema(request_body=MonthSerializer)
    def create_month(self, request):
        serializer = MonthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Oy ma'lumotlarini yangilash
    @action(detail=True, methods=['put'], url_path='update/month')
    @swagger_auto_schema(request_body=MonthSerializer)
    def update_month(self, request, pk=None):
        month = get_object_or_404(Month, pk=pk)
        serializer = MonthSerializer(month, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Oy ma'lumotlarini o'chirish
    @action(detail=True, methods=['delete'], url_path='delete/month')
    def delete_month(self, request, pk=None):
        month = get_object_or_404(Month, pk=pk)
        month.delete()
        return Response({'status': True, 'detail': 'Month muvaffaqiyatli o‘chirildi'}, status=status.HTTP_204_NO_CONTENT)


class PaymentTypeViewSet(viewsets.ViewSet): #To'lov turlarini boshqarish API
    permission_classes = [AdminUser]

    def list(self, request):  # Barcha to‘lov turlarini olish
        types = PaymentType.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(types, request)
        serializer = PaymentTypeSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None): # Bitta to‘lov turi haqida ma’lumot olish
        type = get_object_or_404(PaymentType, pk=pk)
        serializer = PaymentTypeSerializer(type)
        return Response(serializer.data)

    # Yangi to‘lov turi yaratish
    @action(detail=False, methods=['post'], url_path='create/payment-type')
    @swagger_auto_schema(request_body=PaymentTypeSerializer)
    def create_type(self, request):
        serializer = PaymentTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # To‘lov turini yangilash
    @action(detail=True, methods=['put'], url_path='update/payment-type')
    @swagger_auto_schema(request_body=PaymentTypeSerializer)
    def update_type(self, request, pk=None):
        type = get_object_or_404(PaymentType, pk=pk)
        serializer = PaymentTypeSerializer(type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # To‘lov turini o‘chirish
    @action(detail=True, methods=['delete'], url_path='delete/payment-type')
    def delete_type(self, request, pk=None):
        type = get_object_or_404(PaymentType, pk=pk)
        type.delete()
        return Response({'status': True, 'detail': 'PaymentType muvaffaqiyatli o‘chirildi'}, status=status.HTTP_204_NO_CONTENT)


class PaymentViewSet(viewsets.ViewSet): #To'lovlarni boshqarish uchun API
    permission_classes = [AdminUser]


    def list(self, request):  # Barcha to‘lovlarni olish
        payments = Payment.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(payments, request)
        serializer = PaymentSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None): # Bitta to‘lov haqida ma’lumot olish
        payment = get_object_or_404(Payment, pk=pk)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    # Yangi to‘lov qo‘shish
    @action(detail=False, methods=['post'], url_path='create/payment')
    @swagger_auto_schema(request_body=PaymentSerializer)
    def create_payment(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # To‘lovni yangilash
    @action(detail=True, methods=['put'], url_path='update/payment')
    @swagger_auto_schema(request_body=PaymentSerializer)
    def update_payment(self, request, pk=None):
        payment = get_object_or_404(Payment, pk=pk)
        serializer = PaymentSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # To‘lovni o‘chirish
    @action(detail=True, methods=['delete'], url_path='delete/payment')
    def delete_payment(self, request, pk=None):
        payment = get_object_or_404(Payment, pk=pk)
        payment.delete()
        return Response({'status': True, 'detail': 'Payment muvaffaqiyatli o‘chirildi'}, status=status.HTTP_204_NO_CONTENT)
