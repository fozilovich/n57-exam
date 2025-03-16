from django.db import models

from app_common.models import BaseModel
from app_users.models import Teacher


class Course(BaseModel):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

class Subject(BaseModel):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

class TableType(BaseModel):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Table Type'
        verbose_name_plural = 'Table Types'

class Table(BaseModel):
    start_time = models.CharField(max_length=50)
    finish_time = models.CharField(max_length=50)
    room = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    type = models.ForeignKey(TableType, on_delete=models.CASCADE, related_name='tables')

    def __str__(self):
        return f"{self.room} ({self.start_time} - {self.finish_time})"

    class Meta:
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'

class Group(BaseModel):
    title = models.CharField(max_length=100)
    teacher = models.ManyToManyField(Teacher, related_name='groups', blank=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='groups')
    active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    table = models.ForeignKey('Table', on_delete=models.SET_NULL, null=True, blank=True, related_name='groups')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

#Homework
class Homework(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey('app_courses.Course', on_delete=models.CASCADE, related_name='homeworks')
    group = models.ForeignKey('app_courses.Group', on_delete=models.CASCADE, related_name='homeworks')
    teacher = models.ForeignKey('app_users.Teacher', on_delete=models.CASCADE, related_name='homeworks')

    def __str__(self):
        return f"{self.title} - {self.group.title}"

    class Meta:
        verbose_name = 'Homework'
        verbose_name_plural = 'Homeworks'

class HomeworkSubmission(BaseModel):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey('app_users.Student', on_delete=models.CASCADE, related_name='submissions')
    link = models.CharField(max_length=255)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.full_name} - {self.homework.title}"

    verbose_name = 'Homework Submission'
    verbose_name_plural = 'Homework Submissions'

class HomeworkReview(BaseModel):
    submission = models.OneToOneField(HomeworkSubmission, on_delete=models.CASCADE, related_name='review')
    teacher = models.ForeignKey('app_users.Teacher', on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField(null=True, blank=True)
    grade = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Review for {self.submission.student.user.full_name} - {self.submission.homework.title}"

