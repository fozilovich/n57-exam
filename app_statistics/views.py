from datetime import datetime

from django.db.models import Count, Q, Sum
from django.utils.timezone import make_aware
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from app_users.models import Student
from app_statistics.serializers import DateFilterSerializer



class StudentFilterView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=DateFilterSerializer)
    def post(self, request):
        serializer = DateFilterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        start_date = make_aware(datetime.combine(start_date, datetime.min.time()))
        end_date = make_aware(datetime.combine(end_date, datetime.max.time()))

        total_students = Student.objects.count()
        graduated_students = Student.objects.filter(group__active=False, created_at__range=[start_date, end_date]).count()
        studying_students = Student.objects.filter(group__active=True, created_at__range=[start_date, end_date]).count()
        registered_students = Student.objects.filter(created_at__range=[start_date, end_date]).count()

        return Response({
            "total_students": total_students,
            "registered_students": registered_students,
            "studying_students": studying_students,
            "graduated_students": graduated_students,
        }, status=status.HTTP_200_OK)
