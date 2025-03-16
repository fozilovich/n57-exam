from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_attendance.views import StatusViewSet, AttendanceViewSet, StudentAttendanceAPIView

app_name = 'attendances'
router = DefaultRouter()
router.register(r'status', StatusViewSet, basename='status')
router.register('attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('student-attendance/<int:student_id>/', StudentAttendanceAPIView.as_view(), name='student_attendance'),

    path('', include(router.urls)),
]