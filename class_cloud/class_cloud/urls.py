from django.conf.urls import patterns, include, url
from django.contrib import admin
#from assignments.views import assignments
from course.views import courses, assignments
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'class_cloud.views.home', name='home'),
    # url(r'^class_cloud/', include('class_cloud.foo.urls')),
    url(r'^$', courses, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'course/(?P<title>[-\w]+)/(?P<assignment>[-\w]+)/$', 'course.views.assignment', name='courses'),
    url(r'course/(?P<title>[-\w]+)$', 'course.views.course', name='course'),
    url(r'^assignments/$', assignments),
)
