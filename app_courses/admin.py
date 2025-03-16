from django.contrib import admin

from app_courses.models import *

admin.site.register([Course,Subject,TableType,Table,Group,Homework,HomeworkSubmission,HomeworkReview])