from django.contrib import admin
from course.models import Course, Assignment


class CourseAdmin(admin.ModelAdmin):
    #prepopulated_fields = {"description": ("name", )}
    list_display = ('active', 'title')
    list_display_links = ('title',)
    list_editable = ('active',)
    list_filter = ('modified', 'created', 'active')


class AssignmentAdmin(admin.ModelAdmin):
    #TODO change the user field to say Teacher: or Professor:
    list_display = ('name', 'due_date', 'course')
    list_filter = ('modified', 'created', 'active', 'due_date')

admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
