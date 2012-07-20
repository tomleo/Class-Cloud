from django.conf import settings
from django.conf.urls import *
from django.views.generic import list_detail, TemplateView, ListView, DetailView
from django.views.generic.simple import direct_to_template
from django.contrib import admin

admin.autodiscover()

#from course.views import DisplayCourseView, DisplayCourseRedirectView, DetailCourseView
from course.models import Course, Assignment


from django.conf import settings


        
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

    #Index page
    (r'^$', 'course.views.index'),
    (r'^courses/$', 'course.views.index'),
    #(r'^(?P<slug>[-\w]+)/$', 'course.views.course'),
    
    #Courses
    (r'^courses/(?P<course_slug>[-\w]+)/(?P<assignment_slug>[-\w]+)', 'course.views.course_assignment'),
    (r'^courses/(?P<slug>[-\w]+)/$', 'course.views.course'),

    
    (r'^calendar/$', 'course.views.calendar'),
    (r'^passign/$', 'course.views.passign'),
    (r'^course_grades/$', 'course.views.course_grades'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'login.html'} ),

    #Assignment page
    (r'^assignments/(?P<slug>[-\w]+)/$', 'course.views.assignment'),
    (r'^assignments/$', 'course.views.assignments'),
    #(r'^assignments/$', list_detail.object_list, assignment_info),
    #(r'^assignments/(?P<pk>d+)/$', list_detail.object_detail,
    #    assignment_detail),
    
    #Announcement page
    (r'^announcements/$', 'course.views.announcements'),
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    #Course Page
    #(r'^courses/$', list_detail.object_list, course_info),
    #(r'^courses/(?P<slug>[-\w]+)/$', 'course.views.course'),
    
    
    #url(r'^courses/',TemplateView.as_view(template_name="courses.html")),
    
    #url(r'^courses/(?P<pk>\d+)-(?P<slug>[-\w]+)/$',
    #    DetailView.as_view(
    #        context_object_name="courses",
    #        model=Course,
    #        template_name="courses.html"),
    #    name="courses"),
        
    #url(r'^courses/(?P<course_id>\d+)-(?P<slug>[-\w]+)/$',
    #    DisplayCourseView.as_view()),
    
    #url(r'^courses/(?P<course_id>\d+)/$', DisplayCourseRedirectView.as_view()),
    
    #This Query Isn't Working!
    #url(r'^course/(?P<course>[-\w]+)/assignment/(?P<slug>[-\w]+)/$',
    #    'course.views.assignment',
    #    {'queryset': Assignment.objects.all(),
    #     'template_name': 'assignment.html'}),

    #Registration Pages
    (r'^accounts/', include('registration.backends.default.urls')),

    #Test Not sure if this is work keeping for any reason
    #url(r'^test/(?P<pk>\d+)-(?P<slug>[-_\w]+)/$',
    #    DetailView.as_view(
    #        context_object_name="course",
    #        model=Course,
    #        template_name="courses.html"
    #        ), name = "course"),
    
    

    #Admin Site
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
