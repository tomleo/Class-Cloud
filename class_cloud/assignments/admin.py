from django.contrib import admin
from assignments.models import Teacher, Student, Assignment, Course, Grade

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(Course)
admin.site.register(Grade)
