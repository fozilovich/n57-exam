from django.urls import path

from app_statistics.views import StudentFilterView

app_name = 'statistics'

urlpatterns = [
    path('students-statistic/', StudentFilterView.as_view(), name='recent-students'),

]