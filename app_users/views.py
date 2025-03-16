from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema

from app_common.permissions import AdminUser, AdminOrOwner
from app_common.paginations import Pagination
from app_courses.models import Group
from app_courses.serializers import GroupSerializer
from app_users.serializers import TeacherSerializer, UserSerializer, StudentSerializer, UserAndTeacherSerializer, \
    UserAndStudentSerializer, ParentSerializer, UserAllSerializer, GetStudentsByIdsSerializer, \
    GetTeachersByIdsSerializer,HomeworkHistorySerializer
from app_users.models import Teacher,Student,User,Parent,HomeworkHistory


#User
class UserListView(generics.ListAPIView):  # Barcha foydalanuvchilar ro'yxatini olish
    queryset = User.objects.all()
    serializer_class = UserAllSerializer
    pagination_class = Pagination
    permission_classes = [AdminUser]

class UserDetailView(generics.RetrieveAPIView):  # Bitta foydalanuvchi ma'lumotlarini olish
    queryset = User.objects.all()
    queryset = User.objects.all()
    serializer_class = UserAllSerializer
    lookup_field = 'id'
    permission_classes = [AdminUser]

class UserCreateView(generics.CreateAPIView):  # Yangi foydalanuvchi yaratish
    queryset = User.objects.all()
    serializer_class = UserAllSerializer
    permission_classes = [AdminUser]

class UserUpdateView(generics.UpdateAPIView):   # Foydalanuvchi ma'lumotlarini yangilash
    queryset = User.objects.all()
    serializer_class = UserAllSerializer
    lookup_field = 'id'
    permission_classes = [AdminUser]

class UserDeleteView(generics.DestroyAPIView):  # Foydalanuvchini o‘chirish
    queryset = User.objects.all()
    serializer_class = UserAllSerializer
    lookup_field = 'id'
    permission_classes = [AdminUser]

#Teacher
class TeacherListView(ListAPIView):  # Barcha o‘qituvchilar ro‘yxatini olish
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    pagination_class = Pagination
    permission_classes = [AdminUser]

class TeacherUpdateView(UpdateAPIView):  # O‘qituvchi ma'lumotlarini yangilash
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'id'
    permission_classes = [AdminUser]

class TeacherRetrieveAPIView(RetrieveAPIView):  # Bitta o‘qituvchi haqida ma'lumot olish
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'id'
    permission_classes = [AdminOrOwner]

class GetTeachersByIds(APIView):  # Berilgan IDlar bo‘yicha o‘qituvchilarni olish
    permission_classes = [AdminUser]
    @swagger_auto_schema(request_body=GetTeachersByIdsSerializer)
    def post(self, request):
        teacher_ids = request.data.get("teacher_ids", [])

        if not teacher_ids or not isinstance(teacher_ids, list):
            return Response({"error": "teacher_ids ro‘yxati bo‘lishi kerak"}, status=status.HTTP_400_BAD_REQUEST)

        teachers = Teacher.objects.filter(id__in=teacher_ids)
        serializer = TeacherSerializer(teachers, many=True)

        return Response({"teachers": serializer.data}, status=status.HTTP_200_OK)

class TeacherCreateAPIView(APIView):
    permission_classes = [AdminUser]

    @swagger_auto_schema(request_body=UserAndTeacherSerializer)
    def post(self, request):
        user_data = request.data.get('user', {})
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save(is_teacher=True)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        teacher_data = request.data.get('teacher', {})
        teacher_serializer = TeacherSerializer(data=teacher_data)

        if teacher_serializer.is_valid():
            phone = user_data.get('phone')
            user_t = User.objects.get(phone=phone)
            teacher_serializer.validated_data['user'] = user_t
            teacher_serializer.save()
            return Response(teacher_serializer.data, status=status.HTTP_201_CREATED)

        else:
            user.delete()
            return Response(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherGroupsAPIView(APIView):  # O‘qituvchiga tegishli guruhlarni olish
    permission_classes = [AdminOrOwner]

    def get(self, request, teacher_id):
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=404)

        groups = teacher.groups.all()
        serializer = GroupSerializer(groups, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

#Student
class StudentListView(ListAPIView): # Barcha talabalar ro‘yxatini olish
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = Pagination
    permission_classes = [AdminUser]

class StudentUpdateView(UpdateAPIView):  # Talaba ma'lumotlarini yangilash
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'
    permission_classes = [AdminUser]

class StudentRetrieveAPIView(RetrieveAPIView):  # Bitta talaba haqida ma'lumot olish
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'
    permission_classes = [AdminOrOwner]


class GetStudentsByIds(APIView): # Berilgan IDlar bo‘yicha talabalarni olish
    permission_classes = [AdminUser]
    @swagger_auto_schema(request_body=GetStudentsByIdsSerializer)
    def post(self, request):
        student_ids = request.data.get("student_ids", [])

        if not student_ids or not isinstance(student_ids, list):
            return Response({"error": "student_ids ro‘yxati bo‘lishi kerak"}, status=status.HTTP_400_BAD_REQUEST)

        students = Student.objects.filter(id__in=student_ids)
        serializer = StudentSerializer(students, many=True)

        return Response({"students": serializer.data}, status=status.HTTP_200_OK)


class StudentCreateAPIView(APIView):
    permission_classes = [AdminUser]

    @swagger_auto_schema(request_body=UserAndStudentSerializer)
    def post(self, request):
        user_data = request.data.get('user', {})
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save(is_student=True)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        student_data = request.data.get('student', {})
        student_serializer = StudentSerializer(data=student_data)

        if student_serializer.is_valid():
            phone = user_data.get('phone')
            user_s = User.objects.get(phone=phone)
            student_serializer.validated_data['user'] = user_s
            student = student_serializer.save()
        else:
            user.delete()
            return Response(student_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        parent_data = request.data.get('parent', {})
        parent_serializer = ParentSerializer(data=parent_data)

        if parent_serializer.is_valid():
            parent = parent_serializer.save()
            parent.students.add(student)
            return Response(parent_serializer.data, status=status.HTTP_201_CREATED)

        else:
            user.delete()
            return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentGroupsAPIView(APIView):  # Talabaga tegishli guruhlarni olish
    permission_classes = [AdminOrOwner]
    def get(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
        except Teacher.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)

        groups = Group.objects.filter(g_student=student)
        serializer = GroupSerializer(groups, many=True)

        return Response(serializer.data, status=200)

#Parrent
class ParentViewSet(viewsets.ViewSet):
    permission_classes = [AdminUser]

    def list(self, request):
        parents = Parent.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(parents, request)
        serializer = ParentSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        parent = get_object_or_404(Parent, pk=pk)
        serializer = ParentSerializer(parent)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create/parent')
    @swagger_auto_schema(request_body=ParentSerializer)
    def create_parent(self, request):
        serializer = ParentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update/parent')
    @swagger_auto_schema(request_body=ParentSerializer)
    def update_parent(self, request, pk=None):
        parent = get_object_or_404(Parent, pk=pk)
        serializer = ParentSerializer(parent, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete/parent')
    def delete_parent(self, request, pk=None):
        parent = get_object_or_404(Parent, pk=pk)
        parent.delete()
        return Response({'status':True,'detail': 'Parent muaffaqiatli uchirildi'}, status=status.HTTP_204_NO_CONTENT)


class HomeworkHistoryViewSet(viewsets.ModelViewSet): # Uyga vazifalar tarixi bilan ishlash uchun API
    queryset = HomeworkHistory.objects.all()
    serializer_class = HomeworkHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_student:
            return HomeworkHistory.objects.filter(student__user=self.request.user)
        return HomeworkHistory.objects.all()

    @swagger_auto_schema(
        operation_description="Uyga vazifa tarixi yaratish",
        request_body=HomeworkHistorySerializer,
        responses={201: HomeworkHistorySerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Barcha uyga vazifalar ro‘yxatini olish",
        responses={200: HomeworkHistorySerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TeacherGroupStudentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, teacher_id, group_id):
        try:
            teacher = Teacher.objects.get(id=teacher_id)

            if not teacher.course.filter(groups__id=group_id).exists():
                return Response({"error": "This group does not belong to the teacher"}, status=403)

            group = Group.objects.get(id=group_id)
            students = group.g_student.all().values("user__full_name", "user__phone")

            return Response({"group": group.name, "students": list(students)})

        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=404)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=404)




