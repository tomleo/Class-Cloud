
from django.views.generic import list_detail, date_based, TemplateView, RedirectView, DetailView
from django.views.generic.edit import FormView

from course.models import Course, Assignment
# can i simply do from models import Course, Assignment?

from django.shortcuts import render_to_response, RequestContext
#from django.template import Context, loader #Replaced by render_to_response shortcut
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """ Template is passed a context
    
    The context is a dictionary mapping between template variable names and
    Python objects
    """
    courses = Course.objects.all()
    #template = loader.get_template('index.html')
    #context = Context({'courses': courses,})
    #eturn HttpResponse(template.render(context))
    return render_to_response('index.html',
        {'course': courses},
        context_instance=RequestContext(request))
    

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


def course(request, slug):
    courses = Blog.objects.get(slug=slug)
    queryset = Assignment.objects.get_visible().filter(course__slug=slug)
    template_name = 'courses.html'
    return date_based.archive_index(request, queryset, date_field="end_date",
                                    extra_context={ 'course': courses })


def assignment(request, course, slug):
    #template_name = "assignment.html"
    queryset = Assignment.objects.get_visible().filter(course__slug=course)
    return list_detail.object_detail(request, queryset, slug=slug)
