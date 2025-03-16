from rest_framework.routers import DefaultRouter
from django.urls import path, include

from app_courses.views import GroupViewSet, SubjectViewSet, TableViewSet, TableTypeViewSet, CourseViewSet, \
    HomeworkViewSet, HomeworkSubmissionViewSet, HomeworkReviewViewSet, GetGroupByIds

app_name = 'courses'

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'tables', TableViewSet, basename='table')
router.register(r'table-types', TableTypeViewSet, basename='table-type')
router.register('homeworks',HomeworkViewSet,basename='homework')
router.register('homework-submissions',HomeworkSubmissionViewSet,basename='homework-submission')
router.register('homework-reviews',HomeworkReviewViewSet,basename='homework-review')
urlpatterns = [
    path('get-groups-by-ids/',GetGroupByIds.as_view(), name='get-groups-by-ids'),
    path('', include(router.urls)),

]