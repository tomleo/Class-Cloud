from django.conf import settings
from django.conf.urls import *
from django.conf.urls.defaults import *
from django.views.generic import list_detail, TemplateView, ListView, DetailView
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from django.contrib.auth.views import password_reset

admin.autodiscover()

#from course.views import DisplayCourseView, DisplayCourseRedirectView, DetailCourseView
from course.models import Course, Assignment

from django.conf import settings


from django.db.models.signals import post_save
from course.models import UserProfile, UserProfileForm
from django.contrib.auth.models import User

def createUserProfile(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
    
post_save.connect(createUserProfile, sender=User)

#course_info = {
#	"queryset": Course.objects.filter(active=True),
#    "template_name": "courses.html",
#    "template_object_name": "courses",
#    "extra_context": {"assignments": Assignment.objects.filter(active=True)}
#}

#assignment_info = {
#    "queryset": Assignment.objects.filter(active=True),
#    "template_name": "assignments.html",
#    "template_object_name": "assignments",
#}

#assignment_detail = {
#    "queryset":
#    Assignment.objects.filter(active=True).order_by('due_date').reverse(),
#    #The order_by and reverse functions do not seem to be working
#    "template_name": "assignment.html",
#} 

urlpatterns = patterns('',

    #Index page
    #If the index page calls index, then a redirect is required so the link
    #doesn't break
    #url(r'^courses/(?P<course_id>\d+)/$', DisplayCourseRedirectView.as_view()),
    (r'^$', 'course.views.index'),
    
    #Profile
    (r'^profiles/edit/$', 'profiles.views.edit_profile', {'form_class': UserProfileForm }),
    (r'^profiles/$', include('profiles.urls')),
    
    #Grades
    (r'^grades/$', 'course.views.grades'),
    
    #Courses
    (r'^courses/$', 'course.views.index'),
    (r'^courses/(?P<course_slug>[-\w]+)/$', 'course.views.course'),
    
    #Assignment
    (r'^courses/(?P<course_slug>[-\w]+)/(?P<assignment_slug>[-\w]+)/submit/complete/$', 'course.views.course_assignment_complete'),
    (r'^courses/(?P<course_slug>[-\w]+)/(?P<assignment_slug>[-\w]+)/submit/$', 'course.views.course_assignment_submit'),
    #(r'^courses/(?P<course_slug>[-\w]+)/(?P<assignment_slug>[-\w]+)/edit/$', 'course.views.course_assignment_edit'),
    (r'^courses/(?P<course_slug>[-\w]+)/(?P<assignment_slug>[-\w]+)/grade/$', 'course.views.course_assignment_grade'),
    (r'^courses/(?P<course_slug>[-\w]+)/(?P<assignment_slug>[-\w]+)/view/$', 'course.views.course_assignment_view'),
    (r'^courses/(?P<course_slug>[-\w]+)/(?P<assignment_slug>[-\w]+)/$', 'course.views.course_assignment'),
  
    #Calendar
    (r'^calendar/$', 'course.views.calendar'),
    
    #Login & Registration
    (r'^accounts/login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'login.html',
        }
    ),
    (r'^accounts/password/reset/$', password_reset, {'template_name': 'registration/password_reset.html'}),
    (r'^accounts/', include('registration.backends.default.urls')),
    
    #url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
    #(r'^admin/password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    #(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    #(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),

    #Assignment page
    (r'^assignments/(?P<slug>[-\w]+)/$', 'course.views.assignment'),
    (r'^assignments/$', 'course.views.assignments'),
    
    #LOL .php ------------->  :D
    #(r'^assignments/(?P<slug>[-\w]+)/file_upload.php/', 'course.views.assignment'),
    
    #Announcement page
    (r'^announcements/$', 'course.views.announcements'),
    
    #Static Content
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),

    #TEACHER VIEW_______________________________________________________________
    
    #Teacher
    (r'^teacher/$', 'course.views.teacher_index'),
    (r'^teacher/(?P<course_slug>[-\w]+)/annoucement_add/$', 'course.views.annoucement_add'),
    (r'^teacher/(?P<course_slug>[-\w]+)/annoucement_complete/$', 'course.views.annoucement_complete'),
    (r'^teacher/(?P<course_slug>[-\w]+)/assignment_add/$', 'course.views.assignment_add'),
    (r'^teacher/(?P<course_slug>[-\w]+)/assignment_complete/$', 'course.views.assignment_complete'),
    (r'^teacher/(?P<course_slug>[-\w]+)/grade_assignments/(?P<assignment_slug>[-\w]+)/(?P<student_username>[-\w]+)/assignment_graded/', 'course.views.grade_assignment_complete'),
    (r'^teacher/(?P<course_slug>[-\w]+)/grade_assignments/(?P<assignment_slug>[-\w]+)/(?P<student_username>[-\w]+)/$', 'course.views.grade_assignment'),
    (r'^teacher/(?P<course_slug>[-\w]+)/grade_assignments/$', 'course.views.grade_assignments'),
    (r'^teacher/(?P<course_slug>[-\w]+)/edit_course/$', 'course.views.edit_course'),
    (r'^teacher/(?P<course_slug>[-\w]+)/edit_course_complete/$', 'course.views.edit_course_complete'),
    
    (r'^teacher/(?P<course_slug>[-\w]+)/enroll_students/$', 'course.views.enroll_students'),
    (r'^teacher/(?P<course_slug>[-\w]+)/enroll_student/(?P<student>[-\w]+)/$', 'course.views.enroll_student'),
    (r'^teacher/(?P<course_slug>[-\w]+)/enroll_student/(?P<student>[-\w]+)/complete/$', 'course.views.enroll_student_complete'),
    #(r'^teacher/enrollment/requests/$', 'course.views.teacher_enroll'),
    (r'^teacher/(?P<course_slug>[-\w]+)/$', 'course.views.teacher_course'),

    (r'^teacher/add/course/$', 'course.views.add_course'),

    #Admin Site
    url(r'^admin/', include(admin.site.urls)),
)

# This is already implemented above without the check for DEBUG only I called it
# document_root instead of 'serve'...
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
