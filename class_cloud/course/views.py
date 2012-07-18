
from django.views.generic import list_detail, date_based, TemplateView, RedirectView, DetailView
from django.views.generic.edit import FormView

from course.models import Course, Assignment, Grade, StudentGrade
from django.contrib.auth.models import User

from django.shortcuts import render_to_response, RequestContext
#from django.template import Context, loader #Replaced by render_to_response shortcut
from django.http import HttpResponse

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required

def calendar(request):
    return render_to_response('calendar.html',
        context_instance=RequestContext(request))

def passign(request):
    return render_to_response('passign.html',
        context_instance=RequestContext(request))
        
def course_grades(request):
    return render_to_response('course_grades.html',
        context_instance=RequestContext(request))        
        


@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def index(request):
    """ Template is passed a context
    
    The context is a dictionary mapping between template variable names and
    Python objects
    """
    courses = Course.objects.filter(students__username=request.user.username)
    return render_to_response('courses.html',
        {'courses': courses},
        context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def courses(request, slug):
    courses = Course.objects.filter(students__username=request.user.username)
    return render_to_response('courses.html',
        {'courses': courses},
        context_instance=RequestContext(request))
                                    
                                    
@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def course(request, slug):

    selected_course = Course.objects.get(slug=slug)
    course_assignments = Assignment.objects.filter(course=selected_course)
    #grades = Grade.objects.filter(course=selected_course)

    
    template_name = 'course.html'
    return render_to_response(template_name, 
        {'course':selected_course,
         'assignments':course_assignments,
          'grades':class_grades},
        context_instance=RequestContext(request))
    

@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def assignments(request):

    assignment_list = []
    courses = Course.objects.filter(students__username=request.user.username)
    for icourse in courses:
        assignment_list.append(Assignment.objects.get(icourse))
    
    
    return render_to_response('assignments.html',
        {'assignments': assignment_list},
        context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def grades(request):
    pass


def logout_view(request):
    logout(request)
    

#def assignment(request, course, slug):
#    #template_name = "assignment.html"
#    queryset = Assignment.objects.get_visible().filter(course__slug=course)
#    return list_detail.object_detail(request, queryset, slug=slug)


