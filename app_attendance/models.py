from django.db import models

from app_common.models import BaseModel
from app_users.models import Student
from app_courses.models import Group


class Status(BaseModel): #Talabaning davomat holatini bildiruvchi model

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'


class Attendance(BaseModel): #Talabaning guruhdagi davomatini ifodalovchi model.

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='attendance')  # Talabaning qaysi guruhga tegishli ekanligini ko'rsatadi

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='attendance')  # Qaysi talaba ekanligini bildiradi

    status = models.ForeignKey(
        'Status', on_delete=models.CASCADE, related_name='attendance')  # Talabaning holatini bildiradi (Qatnashdi, Kech keldi va h.k.)

    def __str__(self):
        return f"{self.student.user.phone} - {self.group.title}"  # Talabaning telefon raqami va guruh nomini qaytaradi

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"
