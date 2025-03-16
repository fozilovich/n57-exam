from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_attendance.models import Status, Attendance
from app_attendance.serializers import StatusSerializer, AttendanceSerializer
from app_common.paginations import Pagination
from app_common.permissions import AdminUser, AdminOrTeacher
from app_users.models import Student


class StatusViewSet(viewsets.ViewSet): #Status ma'lumotlarini boshqaruvchi ViewSet

    permission_classes = [AdminUser]

    def list(self, request): #Barcha statuslarni ro‘yxat ko‘rinishida chiqaradi

        statuses = Status.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(statuses, request)
        serializer = StatusSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None): #Bitta statusni ID bo‘yicha chiqaradi

        status_obj = get_object_or_404(Status, pk=pk)
        serializer = StatusSerializer(status_obj)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create')
    @swagger_auto_schema(request_body=StatusSerializer)
    def create_status(self, request): #Yangi status yaratish uchun API

        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update')
    @swagger_auto_schema(request_body=StatusSerializer)
    def update_status(self, request, pk=None): #Mavjud statusni yangilash uchun API

        status_obj = get_object_or_404(Status, pk=pk)
        serializer = StatusSerializer(status_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_status(self, request, pk=None): # Statusni o‘chirish uchun API

        status_obj = get_object_or_404(Status, pk=pk)
        status_obj.delete()
        return Response({'status': True, 'detail': 'Status muvaffaqiyatli o‘chirildi'}, status=status.HTTP_204_NO_CONTENT)


class AttendanceViewSet(viewsets.ViewSet): #Davomat ma'lumotlarini boshqaruvchi ViewSet

    permission_classes = [AdminOrTeacher]

    def list(self, request): # Barcha davomat yozuvlarini chiqaradi

        attendances = Attendance.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(attendances, request)
        serializer = AttendanceSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None): #Bitta davomat yozuvini ID bo‘yicha chiqaradi

        attendance = get_object_or_404(Attendance, pk=pk)
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create')
    @swagger_auto_schema(request_body=AttendanceSerializer)
    def create_attendance(self, request): # Yangi davomat yozuvini yaratish uchun API

        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update')
    @swagger_auto_schema(request_body=AttendanceSerializer)
    def update_attendance(self, request, pk=None): # Mavjud davomat yozuvini yangilash uchun API

        attendance = get_object_or_404(Attendance, pk=pk)
        serializer = AttendanceSerializer(attendance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_attendance(self, request, pk=None): #Davomat yozuvini o‘chirish uchun API

        attendance = get_object_or_404(Attendance, pk=pk)
        attendance.delete()
        return Response({'status': True, 'detail': 'Davomat muvaffaqiyatli o‘chirildi'}, status=status.HTTP_204_NO_CONTENT)


class StudentAttendanceAPIView(APIView): # Talabaning davomat ma'lumotlarini ko‘rish uchun API

    permission_classes = [IsAuthenticated]
    pagination_class = Pagination

    def get(self, request, student_id): # Berilgan talabaning davomat statistikasi va foizini qaytaradi
        student = get_object_or_404(Student, id=student_id)

        # Talabaning davomat ma’lumotlarini olish
        attendance_records = student.attendance.all().order_by("-date")
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(attendance_records, request)

        total_classes = student.attendance.count()
        present_count = student.attendance.filter(status="present").count()
        absent_count = student.attendance.filter(status="absent").count()

        # Davomat foizini hisoblash
        attendance_percentage = (present_count / total_classes * 100) if total_classes > 0 else 0

        return paginator.get_paginated_response({
            "student": student.user.full_name,
            "total_classes": total_classes,
            "present": present_count,
            "absent": absent_count,
            "attendance_percentage": f"{attendance_percentage:.2f}%",
            "attendance_records": list(result_page.values("date", "status"))
        })
