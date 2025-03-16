from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

from app_common.models import BaseModel


class UserManager(BaseUserManager): #Foydalanuvchilarni yaratish va boshqarish uchun maxsus UserManager.

    def create_user(self, phone, password=None, **extra_fields): #Oddiy foydalanuvchi yaratish funksiyasi.

        if not phone:
            raise ValueError('Telefon raqami kiritilishi shart')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields): #Superuser (admin) yaratish funksiyasi.

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser is_staff=True bo‘lishi kerak.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser is_superuser=True bo‘lishi kerak.')

        return self.create_user(phone, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin): #Foydalanuvchi modeli. Telefon raqami orqali autentifikatsiya qilinadi.

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$',
        message="Telefon raqami quyidagi formatda bo‘lishi kerak: '9989012345678'. Maksimal 14 ta raqam."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)  # Unikal telefon raqami
    full_name = models.CharField(max_length=50, null=True, blank=True)  # To'liq ism
    is_active = models.BooleanField(default=True)  # Foydalanuvchi aktiv yoki yo‘qligi
    is_staff = models.BooleanField(default=False)  # Admin panelga kirish ruxsati
    is_admin = models.BooleanField(default=False)  # Superuser ruxsati
    is_student = models.BooleanField(default=False)  # Talaba ekanligini belgilash
    is_teacher = models.BooleanField(default=False)  # O‘qituvchi ekanligini belgilash
    created = models.DateTimeField(auto_now_add=True)  # Yaratilgan vaqt
    updated = models.DateTimeField(auto_now=True)  # Yangilangan vaqt

    username = None

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()  # Foydalanuvchi yaratish uchun maxsus manager

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


# Talaba modeli
class Student(BaseModel): # Talaba modeli. Bir foydalanuvchi faqat bitta talabaga tegishli bo‘lishi mumkin.

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ManyToManyField('app_courses.Group', related_name='g_student', blank=True)
    cource = models.ManyToManyField('app_courses.Course', related_name='c_student')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.phone

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'



class Teacher(BaseModel): #O‘qituvchi modeli. Har bir o‘qituvchiga bir foydalanuvchi tegishli bo‘ladi

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    cource = models.ManyToManyField('app_courses.Course', related_name='c_teacher')

    def __str__(self):
        return self.user.phone

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'


# Ota-ona modeli
class Parent(BaseModel): #  Ota-ona modeli. Ota-onalar bir yoki bir nechta talabaga tegishli bo‘lishi mumkin


    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    students = models.ManyToManyField('Student', related_name='parent')
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'



class HomeworkHistory(BaseModel): #Talabaning uy vazifalari bo‘yicha tarixi.

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='homework_history')  # Talaba
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.student.user.phone}"

    class Meta:
        verbose_name = "Homework History"
        verbose_name_plural = "Homework Histories"
