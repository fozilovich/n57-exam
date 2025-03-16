from django.db.models import Count, Q
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_courses.models import Course
from app_common.permissions import AdminUser


class CourseStudentStatisticsView(APIView):

    permission_classes = [AdminUser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Boshlanish sanasi bo‘yicha filter (format: YYYY-MM-DDTHH:MM:SS)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="Tugash sanasi bo‘yicha filter (format: YYYY-MM-DDTHH:MM:SS)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME
            ),
        ]
    )
    def get(self, request):  #Kurslar bo‘yicha talabalarning statistik ma'lumotlarini qaytaradi.


        # URL parametrlaridan boshlanish va tugash sanalarini olish
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        # Agar sanalar berilmagan bo‘lsa, xato qaytariladi
        if not start_date or not end_date:
            return Response(
                {"error": "start_date va end_date berilishi shart"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            start_date = make_aware(parse_datetime(f"{start_date} 00:00:00"))
            end_date = make_aware(parse_datetime(f"{end_date} 23:59:59"))
        except Exception:
            return Response(
                {"error": "Sana formati noto‘g‘ri. YYYY-MM-DD bo‘lishi kerak."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Kurslar bo‘yicha statistik ma'lumotlarni hisoblash
        courses_statistics = (
            Course.objects.annotate(
                total_registered_students=Count(
                    "c_student", filter=Q(c_student__created_at__range=[start_date, end_date])
                ),
                total_studying_students=Count(
                    "c_student", filter=Q(
                        c_student__group__active=True,
                        c_student__created_at__range=[start_date, end_date]
                    )
                ),
                total_graduated_students=Count(
                    "c_student", filter=Q(
                        c_student__group__active=False,
                        c_student__created_at__range=[start_date, end_date]
                    )
                )
            ).values("title", "total_registered_students", "total_studying_students", "total_graduated_students")
        )

        return Response(list(courses_statistics), status=status.HTTP_200_OK)
