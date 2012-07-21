from django.contrib import admin
from course.models import Course, Assignment, Grade, Enrollment, StudentGrade, AssignmentAttempt, SubmittedAssignment, Announcement, Discussion


class CourseAdmin(admin.ModelAdmin):
    #prepopulated_fields = {"description": ("name", )}
    list_display = ('active', 'title')
    list_display_links = ('title',)
    list_editable = ('active',)
    list_filter = ('modified', 'created', 'active')
    prepopulated_fields = {'slug':('title',),}

class AssignmentAdmin(admin.ModelAdmin):
    #TODO change the user field to say Teacher: or Professor:
    list_display = ('name', 'due_date', 'course')
    list_filter = ('modified', 'created', 'active', 'due_date')
    prepopulated_fields = {'slug':('name',),}

class GradeAdmin(admin.ModelAdmin):
    pass

class StudentGradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'grade')
    
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('students', 'course', 'start_date')
    
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    pass
    
class SubmittedAssignmentAdmin(admin.ModelAdmin):
    pass

class AnnouncementAdmin(admin.ModelAdmin):
    pass
    
class DiscussionAdmin(admin.ModelAdmin):
	pass

admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)

admin.site.register(StudentGrade, StudentGradeAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(AssignmentAttempt, AssignmentSubmissionAdmin)

admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(SubmittedAssignment, SubmittedAssignmentAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Discussion, DiscussionAdmin)

