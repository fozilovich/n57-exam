from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from app_courses.models import Group, Subject, Course, Table, TableType, Homework, HomeworkSubmission, HomeworkReview
from app_common.permissions import AdminUser, AdminOrTeacher, AdminOrStudent
from app_common.paginations import Pagination
from app_courses.serializers import GroupSerializer, GroupAddStudent, GroupAddTeacher, SubjectSerializer, \
    CourseSerializer, TableSerializer, TableTypeSerializer, RemoveStudentFromGroupSerializer, \
    RemoveTeacherFromGroupSerializer, HomeworkSerializer, HomeworkSubmissionSerializer, HomeworkReviewSerializer, \
    GetGroupByIdsSerializer
from app_users.models import Student,Teacher

#Group
class GroupViewSet(viewsets.ViewSet):
    permission_classes = [AdminUser]

    def list(self, request):
        groups = Group.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(groups, request)
        serializer = GroupSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create/group')
    @swagger_auto_schema(request_body=GroupSerializer)
    def create_group(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update/group')
    @swagger_auto_schema(request_body=GroupSerializer)
    def update_group(self, request, pk=None):
        department = get_object_or_404(Group, pk=pk)
        serializer = GroupSerializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete/group')
    def delete_group(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        group.delete()
        return Response({'status':True,'detail': 'Group muaffaqiyatli uchirildi'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='add-student')
    @swagger_auto_schema(request_body=GroupAddStudent,)
    def add_student(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        serializer = GroupAddStudent(data=request.data)

        if serializer.is_valid():
            student_id = serializer.validated_data['student_id']
            student = get_object_or_404(Student, pk=student_id)
            student.group.add(group)
            student.save()

            return Response({'status':True,'detail': f'Student {student.user.full_name} - guruhga qushildi {group.title}'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='remove-student')
    @swagger_auto_schema(request_body=RemoveStudentFromGroupSerializer,)
    def remove_student(self, request,pk=None):
        group = get_object_or_404(Group, pk=pk)
        student_id = request.data.get("student_id")

        if not student_id:
            return Response({"status": False, "detail": "student_id kerak"}, status=400)
        try:
            student = Student.objects.get(id=student_id)

            if student.group.filter(id=group.id).exists():
                student.group.remove(group)
                return Response({"status": True, "detail": f"Student {student.user.full_name} - guruhdan chiqarildi."},
                                status=200)
            return Response({"status": False, "detail": "Bu student ushbu guruhga tegishli emas."}, status=400)

        except Student.DoesNotExist:
            return Response({"status": False, "detail": "Student topilmadi."}, status=404)

    @action(detail=True, methods=['post'], url_path='add-teacher')
    @swagger_auto_schema(request_body=GroupAddTeacher, )
    def add_teacher(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        serializer = GroupAddTeacher(data=request.data)

        if serializer.is_valid():
            teacher_id = serializer.validated_data['teacher_id']
            teacher = get_object_or_404(Teacher, pk=teacher_id)
            teacher.groups.add(group)
            teacher.save()

            return Response(
                {'status': True, 'detail': f'Teacher {teacher.user.phone} - guruhga qushildi {group.title}'},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='remove-teacher')
    @swagger_auto_schema(request_body=RemoveTeacherFromGroupSerializer,)
    def remove_teacher(self, request,pk=None):
        group = get_object_or_404(Group, pk=pk)
        teacher_id = request.data.get("teacher_id")

        if not teacher_id:
            return Response({"status": False, "detail": "teacher_id kerak"}, status=400)
        try:
            teacher = Teacher.objects.get(id=teacher_id)

            if teacher.groups.filter(id=group.id).exists():
                teacher.groups.remove(group)
                return Response({"status": True, "detail": f"Teacher {teacher.user.full_name} - guruhdan chiqarildi."},
                                status=200)
            return Response({"status": False, "detail": "Bu teacher ushbu guruhga tegishli emas."}, status=400)

        except Student.DoesNotExist:
            return Response({"status": False, "detail": "Teacher topilmadi."}, status=404)

class GetGroupByIds(APIView):
    permission_classes = [AdminUser]
    @swagger_auto_schema(request_body=GetGroupByIdsSerializer)
    def post(self, request):
        group_ids = request.data.get("group_ids", [])

        if not group_ids or not isinstance(group_ids, list):
            return Response({"error": "group_ids ro‘yxati bo‘lishi kerak"}, status=status.HTTP_400_BAD_REQUEST)

        groups = Group.objects.filter(id__in=group_ids)
        serializer = GroupSerializer(groups, many=True)

        return Response({"groups": serializer.data}, status=status.HTTP_200_OK)

#Subject
class SubjectViewSet(viewsets.ViewSet):
    permission_classes = [AdminUser]

    def list(self, request):
        subjects = Subject.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(subjects, request)
        serializer = SubjectSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        subject = get_object_or_404(Subject, pk=pk)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create/subject')
    @swagger_auto_schema(request_body=SubjectSerializer)
    def create_subject(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update/subject')
    @swagger_auto_schema(request_body=SubjectSerializer)
    def update_subject(self, request, pk=None):
        subject = get_object_or_404(Subject, pk=pk)
        serializer = SubjectSerializer(subject, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete/subject')
    def delete_subject(self, request, pk=None):
        subject = get_object_or_404(Subject, pk=pk)
        subject.delete()
        return Response({'status':True,'detail': 'Subject muaffaqiyatli uchirildi'}, status=status.HTTP_204_NO_CONTENT)

#course
class CourseViewSet(viewsets.ViewSet):
    permission_classes = [AdminUser]

    def list(self, request):
        courses = Course.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(courses, request)
        serializer = CourseSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        serializer = SubjectSerializer(course)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create/course')
    @swagger_auto_schema(request_body=CourseSerializer)
    def create_course(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update/course')
    @swagger_auto_schema(request_body=CourseSerializer)
    def update_course(self, request, pk=None):
        course = get_object_or_404(Subject, pk=pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete/course')
    def delete_course(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return Response({'status':True,'detail': 'Cource muaffaqiyatli uchirildi'}, status=status.HTTP_204_NO_CONTENT)

#Table
class TableViewSet(viewsets.ViewSet):
    permission_classes = [AdminUser]

    def list(self, request):
        tables = Table.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(tables, request)
        serializer = TableSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        table = get_object_or_404(Table, pk=pk)
        serializer = TableSerializer(table)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create/table')
    @swagger_auto_schema(request_body=TableSerializer)
    def create_table(self, request):
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update/table')
    @swagger_auto_schema(request_body=TableSerializer)
    def update_table(self, request, pk=None):
        table = get_object_or_404(Table, pk=pk)
        serializer = TableSerializer(table, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete/table')
    def delete_table(self, request, pk=None):
        table = get_object_or_404(Table, pk=pk)
        table.delete()
        return Response({'status':True,'detail': 'Table muaffaqiyatli uchirildi'}, status=status.HTTP_204_NO_CONTENT)

#TableType
class TableTypeViewSet(viewsets.ViewSet):
    permission_classes = [AdminUser]

    def list(self, request):
        tabletypes = TableType.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(tabletypes, request)
        serializer = TableTypeSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        tabletype = get_object_or_404(TableType, pk=pk)
        serializer = TableTypeSerializer(tabletype)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create/tabletype')
    @swagger_auto_schema(request_body=TableTypeSerializer)
    def create_tabletype(self, request):
        serializer = TableTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update/tabletype')
    @swagger_auto_schema(request_body=TableTypeSerializer)
    def update_tabletype(self, request, pk=None):
        tabletype = get_object_or_404(TableType, pk=pk)
        serializer = TableTypeSerializer(tabletype, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete/tabletype')
    def delete_tabletype(self, request, pk=None):
        tabletype = get_object_or_404(TableType, pk=pk)
        tabletype.delete()
        return Response({'status':True,'detail': 'TableType muaffaqiyatli uchirildi'}, status=status.HTTP_204_NO_CONTENT)

#Homework
class HomeworkViewSet(viewsets.ViewSet):
    permission_classes = [AdminOrTeacher]

    def list(self, request):
        homeworks = Homework.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(homeworks, request)
        serializer = HomeworkSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        homework = get_object_or_404(Homework, pk=pk)
        serializer = HomeworkSerializer(homework)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create/homework')
    @swagger_auto_schema(request_body=HomeworkSerializer)
    def create_homework(self, request):
        serializer = HomeworkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['teacher'] = request.user.teacher
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update/homework')
    @swagger_auto_schema(request_body=HomeworkSerializer)
    def update_homework(self, request, pk=None):
        homework = get_object_or_404(TableType, pk=pk)
        serializer = TableTypeSerializer(homework, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete/homework')
    def delete_homework(self, request, pk=None):
        homework = get_object_or_404(Homework, pk=pk)
        homework.delete()
        return Response({'status':True,'detail': 'Homework muaffaqiyatli uchirildi'}, status=status.HTTP_204_NO_CONTENT)

#HomeworkReview
class HomeworkReviewViewSet(viewsets.ViewSet):
    permission_classes = [AdminOrTeacher]

    def list(self, request):
        homeworkreviews = HomeworkReview.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(homeworkreviews, request)
        serializer = HomeworkReviewSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        homeworkreview = get_object_or_404(HomeworkReview, pk=pk)
        serializer = HomeworkReviewSerializer(homeworkreview)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create/homework-review')
    @swagger_auto_schema(request_body=HomeworkReviewSerializer)
    def create_homeworkreview(self, request):
        serializer = HomeworkReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['teacher'] = request.user.teacher
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update/homework-review')
    @swagger_auto_schema(request_body=HomeworkReviewSerializer)
    def update_homeworkreview(self, request, pk=None):
        homeworkreview = get_object_or_404(HomeworkReviewSerializer, pk=pk)
        serializer = HomeworkReviewSerializer(homeworkreview, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete/homework-review')
    def delete_homeworkreview(self, request, pk=None):
        homeworkreview = get_object_or_404(HomeworkReviewSerializer, pk=pk)
        homeworkreview.delete()
        return Response({'status':True,'detail': 'HomeworkReview muaffaqiyatli uchirildi'}, status=status.HTTP_204_NO_CONTENT)

#HomeworkSubmission
class HomeworkSubmissionViewSet(viewsets.ViewSet):
    permission_classes = [AdminOrStudent]

    def list(self, request):
        homeworksubmissions = HomeworkSubmission.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(homeworksubmissions, request)
        serializer = HomeworkSubmissionSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        homeworksubmission = get_object_or_404(HomeworkSubmission, pk=pk)
        serializer = HomeworkSubmissionSerializer(homeworksubmission)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create/homework-submission')
    @swagger_auto_schema(request_body=HomeworkSubmissionSerializer)
    def create_homeworksubmission(self, request):
        serializer = HomeworkSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['student'] = request.user.student
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update/homework-submission')
    @swagger_auto_schema(request_body=HomeworkSubmissionSerializer)
    def update_homeworksubmission(self, request, pk=None):
        homeworksubmission = get_object_or_404(HomeworkSubmission, pk=pk)
        serializer = HomeworkSubmissionSerializer(homeworksubmission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete/homework-submission')
    def delete_homeworksubmission(self, request, pk=None):
        homeworksubmission = get_object_or_404(HomeworkSubmission, pk=pk)
        homeworksubmission.delete()
        return Response({'status':True,'detail': 'HomeworkSubmission successful launches'}, status=status.HTTP_204_NO_CONTENT)
