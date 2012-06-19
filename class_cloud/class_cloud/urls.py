from django.conf.urls import *
from django.views.generic import list_detail, TemplateView
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

#from course.views import courses, assignments
from course.views import DisplayCourseView, DisplayCourseRedirectView

from course.models import Course, Assignment

course_info = {
	"queryset": Course.objects.filter(active=True),
}

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^courses/(?P<course_id>\d+)-(?P<slug>[-\w]+)/$',
        DisplayCourseView.as_view()),
    url(r'^courses/(?P<course_id>\d+)/$', DisplayCourseRedirectView.as_view()),
	url(r'^$', TemplateView.as_view(template_name="courses.html")),
#	url(
#		r'^$', 
#		list_detail.object_list, 
#		course_info, 
#		name="home",
#		direct_to_template,
#		('template': 'courses.html'),
#	),
#	url(r'^course/(?P<slug>[-\w]+)/$', 'course.views.course', name="course"),
#
#	url(r'^courses/$', ListView.as_view(
#		model=Course,
#		queryset=Course.objects.filter(active=True),
#		template_name='courses.html',
#		context_object_name="course_list",
#	)),
#	url(r'^assignments/$', ListView.as_view(
#		model=Assignment,
#		queryset=Assignment.objects.order_by("-end_date"),
#		template_name="assignment_list.html",
#		context_object_name="assignment_list",
#	)),
#	url(r'^test/$', ListView.as_view(
#		model=Course,
#		template_name="assignments_by_course.html",
#		context_object_name="assignment_list",
#	)),

    #url(r'^$', 'course.views.course_index', name="home"),
    #url(r'^$', courses, name='home'),
    
    #url(r'course/(?P<title>[-\w]+)/(?P<assignment>[-\w]+)/$', 'course.views.assignment', name='courses'),
    #url(r'course/(?P<title>[-\w]+)$', 'course.views.course', name='course'),
    #url(r'^assignments/$', assignments),
)
