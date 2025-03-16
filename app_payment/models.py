from django.db import models

from app_common.models import BaseModel
from app_users.models import Student
from app_courses.models import Group


class Month(BaseModel): # Oylarni saqlash uchun model
    title = models.CharField(max_length=128)  # Oy nomini saqlovchi maydon

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'month'
        verbose_name_plural = 'months'


class PaymentType(BaseModel): # To'lov turlarini saqlash uchun model
    title = models.CharField(max_length=255)  # To‘lov turini saqlovchi maydon

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'payment type'
        verbose_name_plural = 'payment types'


class Payment(BaseModel): # Talabaning to'lovlarini saqlash uchun model
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,  # Agar talaba o‘chirilsa, uning to‘lovlari ham o‘chadi
        related_name='payment'
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='payment',
        null=True, blank=True
    )

    month = models.ForeignKey(
        Month,
        on_delete=models.CASCADE,  # Oy o‘chirilsa, unga tegishli to‘lovlar ham o‘chadi
        related_name='payment',
        null=True, blank=True
    )

    payment_type = models.ForeignKey(
        PaymentType,
        on_delete=models.CASCADE,  # To‘lov turi o‘chirilsa, unga tegishli to‘lovlar ham o‘chadi
        related_name='payment'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.student.user.full_name} - {self.price} UZS ({self.payment_type.title})"

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
