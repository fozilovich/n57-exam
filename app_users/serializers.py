from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from app_users.models import Teacher, User, Student, Parent, HomeworkHistory


class UserAllSerializer(serializers.ModelSerializer): #Foydalanuvchilarning barcha ma'lumotlarini qaytaruvchi serializer
    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer): #Foydalanuvchini yaratish va tahrirlash uchun serializer

    class Meta:
        model = User
        fields = ("id", "password", "full_name", "phone")

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)


class TeacherSerializer(serializers.ModelSerializer): #O'qituvchilar uchun serializer
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Teacher
        fields = ("id", "user", "cource", "description")


class StudentSerializer(serializers.ModelSerializer): #Talabalar uchun serializer
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Student
        fields = ("id", "user", "group", "cource", "description")


class ParentSerializer(serializers.ModelSerializer): #Ota-onalar uchun serializer
    students = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Student.objects.all()
    )

    class Meta:
        model = Parent
        fields = ("id", "name", "surname", "address", "phone", "description", "students")


class GetStudentsByIdsSerializer(serializers.Serializer): #Talabalarni ID bo‘yicha olish uchun serializer
    student_ids = serializers.ListField(child=serializers.IntegerField())


class GetTeachersByIdsSerializer(serializers.Serializer): #O‘qituvchilarni ID bo‘yicha olish uchun serializer
    teacher_ids = serializers.ListField(child=serializers.IntegerField())


class UserAndTeacherSerializer(serializers.ModelSerializer): #Foydalanuvchi va o‘qituvchi ma'lumotlarini qaytaruvchi serializer
    user = UserSerializer()
    teacher = TeacherSerializer()

    class Meta:
        model = Teacher
        fields = ("user", "teacher")


class UserAndStudentSerializer(serializers.ModelSerializer): #Foydalanuvchi, talaba va ota-ona ma'lumotlarini qaytaruvchi serializer
    user = UserSerializer()
    student = StudentSerializer()

    class Meta:
        model = Student
        fields = ("user", "student")


class HomeworkHistorySerializer(serializers.ModelSerializer): #Uy vazifalari tarixini ko'rsatish uchun serializer
    class Meta:
        model = HomeworkHistory
        fields = "__all__"
