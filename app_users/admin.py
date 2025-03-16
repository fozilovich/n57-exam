from django.contrib import admin

from app_courses.models import Homework
from app_users.models import *

admin.site.register([User,Student,Teacher,Parent,HomeworkHistory])
