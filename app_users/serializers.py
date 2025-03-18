from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from app_users.models import Teacher, User, Student, Parent


class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "password", "full_name", "phone")

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Teacher
        fields = ('id', 'user', 'cource', 'description')


class StudentSerializer(serializers.ModelSerializer): #Talabalar uchun serializer
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Student
        fields = ("id", "user", "group", "cource", "description")


class ParentSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Parent
        fields = ('id', 'name', 'surname', 'address', 'phone', 'description', 'students')


class GetStudentsByIdsSerializer(serializers.Serializer):
    student_ids = serializers.ListField(child=serializers.IntegerField())


class GetTeachersByIdsSerializer(serializers.Serializer):
    teacher_ids = serializers.ListField(child=serializers.IntegerField())


class UserAndTeacherSerializer(serializers.Serializer):
    user = UserSerializer()
    teacher = TeacherSerializer()


class UserAndStudentSerializer(serializers.Serializer):
    user = UserSerializer()
    student = StudentSerializer()

