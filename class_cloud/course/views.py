import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import Course, Assignment


def assignments(request):
    list_of_assignments = []
    for assignment in Assignment.objects.all():
        if assignment.active:
            list_of_assignments.append(assignment)
    return render_to_response('assignments.html', {
        'list_assignments': list_of_assignments,
    })


def courses(request):
    list_of_courses = Course.objects.all()
    #list_of_courses = []
    #for course in Course.objects.all():
    #    if course.active:
    #        list_of_courses.append(course)
    return render_to_response('course.html', {
        'list_courses': list_of_courses,
    })


def course(request, title):
    course = get_object_or_404(Course, active=True, title=title)
    return render_to_response('course.html', {
        'course': course
    })


def assignment(request, course, name):
    _assignment = get_object_or_404(Assignment, active=True,
                                    publish_at__lte=datetime.datetime.now(),
                                    name=name)
    return render_to_response('assignment.html', {
        'assignment': _assignment,
        }, context_instance=RequestContext(request))
