
from django.views.generic import list_detail, date_based, TemplateView, RedirectView, DetailView
from django.views.generic.edit import FormView

from course.models import Course, Assignment, Grade
# can i simply do from models import Course, Assignment?

from django.shortcuts import render_to_response, RequestContext
#from django.template import Context, loader #Replaced by render_to_response shortcut
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from django.contrib.auth import login

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required


def group_required(*group_names):
    """This function decorator is by msanders via 
    http://djangosnippets.org/snippets/1703/"""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)


#@login_required
#@user_passes_test(lambda u: u.has_perm('course.view_course'))
@login_required
#@permission_required('course.view_course')
@group_required('student', 'teacher')
def index(request):
    """ Template is passed a context
    
    The context is a dictionary mapping between template variable names and
    Python objects
    """
    courses = Course.objects.all()
    #template = loader.get_template('index.html')
    #context = Context({'courses': courses,})
    #eturn HttpResponse(template.render(context))
    return render_to_response('courses.html',
        {'courses': courses},
        context_instance=RequestContext(request))

@login_required
def courses(request, slug):
    courses = Course.objects.all()
    return render_to_response('courses.html',
        {'courses': courses},
        context_instance=RequestContext(request))
                                    
@login_required
def course(request, slug):
    selected_course = Course.objects.get(slug=slug)
    #course_assignments = Assignment.objects.get(course.slug=selected_course.slug)
    course_assignments = Assignment.objects.filter(course=selected_course)
    grades = Grade.objects.filter(course=selected_course)
    
    courseAndGrade = []
    
    
    template_name = 'course.html'
    return render_to_response(template_name, {'course':selected_course, 'assignments':course_assignments}, context_instance=RequestContext(request))
    

@login_required
def assignments(request):
    assignments = Assignment.objects.all()
    return render_to_response('assignments.html',
        {'assignments': assignments},
        context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    

class DetailCourseView(DetailView):
    
    template_name = "courses.html"
    model = Course

    def get_context_data(self, **kwargs):
        context = super(DetailCourseView, self).get_context_data(**kwargs)
        context['course'] = Course.objects.all()
        return context

class DisplayCourseView(TemplateView):
    template_name = "course.html"

    def get_context_data(self, **kwargs):
        context = super(DisplayCourseView, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk=self.kwargs.get('course_id',
                                                                        None))
        return context


class DisplayCourseRedirectView(RedirectView):
   
    def get(self, request, *args, **kwargs):
        course_id = self.kwargs.get('course_id', None)
        course = Course.objects.get(pk=course_id)
        self.url = '/courses/%s-%s' % (course.id, course.slug)
        return super(DisplayCourseRedirectView, self).get(self, request, *args, **kwargs)



def assignment(request, course, slug):
    #template_name = "assignment.html"
    queryset = Assignment.objects.get_visible().filter(course__slug=course)
    return list_detail.object_detail(request, queryset, slug=slug)
