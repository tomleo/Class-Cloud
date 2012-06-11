from django.conf.urls import patterns, include, url
from django.contrib import admin
from assignments.views import assignments

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'class_cloud.views.home', name='home'),
    # url(r'^class_cloud/', include('class_cloud.foo.urls')),

    url(r'^assignments/$', assignments),
    url(r'^admin/', include(admin.site.urls)),
)
