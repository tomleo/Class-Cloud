import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import list_detail, DetailView

from annoying.decorators import render_to

from models import Course, Assignment

class CourseDetailView(DetailView):

    context_object_name = "course"
    model = Course

    def get_context_data(self, **kwargs):
        #this calls the base implementation to get context
        context = super(CourseDetailView, self).get_context_data(**kwargs)

        context['course_list'] = Course.objects.filter(active=True)
        return context

class AssignmentDetailView(DetailView):

    context_object_name = "assignment"
    model = Assignment

    def get_context_data(self, **kwargs):
        context = super(AssignmentDetailView, self).get_context_data(**kwargs)

        context['assignment_list'] = Assignment.objects.all()
        return context

def assignments(request):
    list_of_assignments = []
    for assignment in Assignment.objects.all():
        if assignment.active:
            list_of_assignments.append(assignment)
    return render_to_response('assignments.html', {
        'list_assignments': list_of_assignments,
    })

#@render_to('index.html')
def course_index(request):
    #courses = Course.objects.filter(active=True)
    queryset = Course.objects.filter(active=True)

    return list_detail.object_detail(queryset=queryset)
    #return { 'courses': courses }

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
