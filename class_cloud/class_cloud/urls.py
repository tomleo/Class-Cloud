from django.conf.urls import *
from django.views.generic import list_detail, TemplateView, ListView, DetailView
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

from course.views import DisplayCourseView, DisplayCourseRedirectView, DetailCourseView
from course.models import Course, Assignment

course_info = {
	"queryset": Course.objects.filter(active=True),
    "template_name": "courses.html",
    "template_object_name": "courses",
    "extra_context": {"assignments": Assignment.objects.filter(active=True)}
}

assignment_info = {
    "queryset": Assignment.objects.filter(active=True),
    "template_name": "assignments.html",
    "template_object_name": "assignments",
}

assignment_detail = {
    "queryset":
    Assignment.objects.filter(active=True).order_by('due_date').reverse(),
    #The order_by and reverse functions do not seem to be working
    "template_name": "assignment.html",
} 

urlpatterns = patterns('',

    (r'^$', 'course.views.index'),
    (r'^home/$', 'course.views.index'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'login.html'} ),


    (r'^assignments/$', list_detail.object_list, assignment_info),
    # /assignments/<id>  DOES NOT WORK!
    (r'^assignments/(?P<pk>d+)/$', list_detail.object_detail,
        assignment_detail),
    (r'^courses/$', list_detail.object_list, course_info),

    #url(r'^$', ListView.as_view(
    #    model = Course,
    #    context_object_name = "courses",
    #    queryset = Course.objects.all(),
    #    template_name="index.html",
    #),name="courses_home"),
    

#    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$',
#        DetailView.as_view(
#            context_object_name="course",
#            model=Course,
#            template_name="course.html"),
#        name="course"),
    url(r'^test/(?P<pk>\d+)-(?P<slug>[-_\w]+)/$',
        DetailView.as_view(
            context_object_name="course",
            model=Course,
            template_name="courses.html"
            ), name = "course"),
        #DetailCourseView.as_view(),
        #'course-detail'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^courses/',TemplateView.as_view(template_name="courses.html")),
    url(r'^courses/(?P<pk>\d+)-(?P<slug>[-\w]+)/$',
        DetailView.as_view(
            context_object_name="courses",
            model=Course,
            template_name="courses.html"),
        name="courses"),
    url(r'^courses/(?P<course_id>\d+)-(?P<slug>[-\w]+)/$',
        DisplayCourseView.as_view()),
    url(r'^courses/(?P<course_id>\d+)/$', DisplayCourseRedirectView.as_view()),
	

    #This Query Isn't Working!
    url(r'^course/(?P<course>[-\w]+)/assignment/(?P<slug>[-\w]+)/$',
        'course.views.assignment',
        {'queryset': Assignment.objects.all(),
         'template_name': 'assignment.html'}),

    #url(r'course/(?P<title>[-\w]+)/(?P<assignment>[-\w]+)/$', 'course.views.assignment', name='courses'),
    #url(r'course/(?P<title>[-\w]+)$', 'course.views.course', name='course'),
    #url(r'^assignments/$', assignments),
)
