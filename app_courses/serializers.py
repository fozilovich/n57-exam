from rest_framework import serializers
from app_courses.models import (
    Group, Subject, Course, Table, TableType,
    Homework, HomeworkSubmission, HomeworkReview
)

class GroupSerializer(serializers.ModelSerializer): # Guruh modeli uchun serializer
    class Meta:
        model = Group
        fields = '__all__'


class GetGroupByIdsSerializer(serializers.Serializer): # Berilgan ID'lar bo'yicha guruhlarni olish uchun serializer
    group_ids = serializers.ListField(child=serializers.IntegerField())


class SubjectSerializer(serializers.ModelSerializer): # Fan modeli uchun serializer
    class Meta:
        model = Subject
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer): # Kurs modeli uchun serializer
    class Meta:
        model = Course
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer): # Jadval modeli uchun serializer
    class Meta:
        model = Table
        fields = '__all__'


class TableTypeSerializer(serializers.ModelSerializer): # Jadval turi modeli uchun serializer
    class Meta:
        model = TableType
        fields = '__all__'


class HomeworkSerializer(serializers.ModelSerializer): # Uyga vazifa modeli uchun serializer
    class Meta:
        model = Homework
        fields = '__all__'
        extra_kwargs = {'teacher': {'read_only': True}}  # O'qituvchi maydonini faqat o'qish uchun qilish


class HomeworkSubmissionSerializer(serializers.ModelSerializer): # Uyga vazifa topshirish modeli uchun serializer
    class Meta:
        model = HomeworkSubmission
        fields = '__all__'
        extra_kwargs = {
            'student': {'read_only': True},  # Talabani faqat o'qish mumkin
            'is_checked': {'read_only': True}  # Tekshirilgan statusini faqat o'qish mumkin
        }


class HomeworkReviewSerializer(serializers.ModelSerializer): # Uyga vazifa baholash modeli uchun serializer
    class Meta:
        model = HomeworkReview
        fields = '__all__'
        extra_kwargs = {
            'teacher': {'read_only': True}  # O'qituvchi maydonini faqat o'qish uchun qilish
        }


class RemoveStudentFromGroupSerializer(serializers.Serializer): # Guruhdan talabani olib tashlash uchun serializer
    student_id = serializers.IntegerField()


class RemoveTeacherFromGroupSerializer(serializers.Serializer): # Guruhdan o‘qituvchini olib tashlash uchun serializer
    teacher_id = serializers.IntegerField()


class GroupAddStudent(serializers.Serializer): # Guruhga talaba qo'shish uchun serializer
    student_id = serializers.IntegerField()


class GroupAddTeacher(serializers.Serializer): # Guruhga o‘qituvchi qo'shish uchun serializer
    teacher_id = serializers.IntegerField()
