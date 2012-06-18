from django.conf.urls import patterns, include, url
from django.views.generic import ListView
#from django.contrib.generic import list_detail
from django.contrib import admin

admin.autodiscover()

from course.views import courses, assignments
from course.models import Course, Assignment

course_info = {
	"queryset": Course.objects.filter(active=True),
}

urlpatterns = patterns('',
	url(r'^courses/$', ListView.as_view(
		model=Course,
		queryset=Course.objects.filter(active=True),
		template_name='courses.html',
		context_object_name="course_list",
	)),
	url(r'^assignments/$', ListView.as_view(
		model=Assignment,
		queryset=Assignment.objects.order_by("-end_date"),
		template_name="assignment_list.html",
		context_object_name="assignment_list",
	)),

    #url(r'^$', 'course.views.course_index', name="home"),
    #url(r'^$', courses, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'course/(?P<title>[-\w]+)/(?P<assignment>[-\w]+)/$', 'course.views.assignment', name='courses'),
    #url(r'course/(?P<title>[-\w]+)$', 'course.views.course', name='course'),
    #url(r'^assignments/$', assignments),
)
