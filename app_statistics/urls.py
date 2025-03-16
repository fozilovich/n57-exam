from django.urls import path

from app_statistics.views import CourseStudentStatisticsView

app_name = 'statistics'

urlpatterns = [
    path('students-statistic/', CourseStudentStatisticsView.as_view(), name='recent-students'),

]