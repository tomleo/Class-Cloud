
from django.views.generic import list_detail, date_based, TemplateView, RedirectView, DetailView
from django.views.generic.edit import FormView

from course.models import Course, Assignment, Grade, StudentGrade, SubmittedAssignment, Announcement, Discussion
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

def course_test(request, course_slug):
    
    selected_course = Course.objects.get(slug=course_slug)
    course_assignments = Assignment.objects.filter(course=selected_course)
    
    import pdb; pdb.set_trace()
    
    return HttpResponse(course_assignments)
    

@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def course(request, course_slug):

    # Assignments Not Submitted
    # Assignments Submitted
    # Assignments Submitted and Graded

    selected_course = Course.objects.get(slug=course_slug)

    # Need to further filter this by due dates and wheather the assignment is active
    course_assignments = Assignment.objects.filter(course=selected_course)
    
    course_announcements = Announcement.objects.filter(course = selected_course)
    course_discussions = Discussion.objects.filter(course = selected_course)
    
    submitted = SubmittedAssignment.objects.filter(student__username=request.user.username)
    
    # all grades associated with given course and user
    student_grades = StudentGrade.objects.filter(student__username=request.user.username,
                                          assignment__course=selected_course)

    # Don't think this is being used...?
    #submitted_and_graded = []
    #for submission in submitted:
    #    if submission.assignment in [a.assignment for a in student_grades]:
    #        submitted_and_graded.append(submission.assignment)
   
    a_graded = []
    a_submitted = []
    a_uncomplete = []
   
    for submission in submitted:
        for student_grade in student_grades:
            if submission.assignment == student_grade.assignment:
                a_graded.append((student_grade.grade, submission))
        
    # Find submitted assignments that are not graded
    for submission in submitted:
        if submission.assignment not in [a[1].assignment for a in a_graded]:
            if submission.assignment.course == selected_course:
                a_submitted.append(submission)
    
    # Find assignments that have not been submitted
    for assignment in course_assignments:
        if assignment not in [i[1].assignment for i in a_graded]:
            if assignment not in [a.assignment for a in a_submitted]:
                a_uncomplete.append(assignment)
    
    template_name = 'course.html'
    return render_to_response(template_name, 
        {'course':selected_course,
         'assignments_graded':a_graded,
         'assignments_submitted':a_submitted,
         'assignments_inbox':a_uncomplete,
         'announcements':course_announcements,
         'discussions' :course_discussions,
         'grades':student_grades},
         context_instance=RequestContext(request))
    

@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def assignments(request):

    assignment_list = []
    courses = []
    courses.extend(Course.objects.filter(students__username=request.user.username))
    
    for icourse in courses:
        course_assignments = Assignment.objects.filter(course=icourse)
        assignment_list.extend(course_assignments)
    
    return render_to_response('assignments.html',
        {'assignments': assignment_list},
        context_instance=RequestContext(request))
       
 
@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def assignment(request, slug):

    a = Assignment.objects.get(slug=slug)
    return render_to_response('assignment.html',
        {'assignment':a},
        context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def course_assignment(request, course_slug, assignment_slug):
    a = Assignment.objects.get(slug=assignment_slug)
    return render_to_response('assignment.html',
        {'assignment':a},
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

@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def announcements(request):

    announcement_list = []
    courses = []
    courses.extend(Course.objects.filter(students__username=request.user.username))
    
    for icourse in courses:
        course_announcements = Announcement.objects.filter(course=icourse)
        announcement_list.extend(course_announcements)
    
    return render_to_response('announcements.html',
        {'announcements': announcement_list},
        context_instance=RequestContext(request))

       
#we might not need this!!
def discussions(request):
	discussion_list = []
	courses = []
	courses.extend(Course.objects.filter(students__username=request.user.username))
	for icourse in courses:
		course_discussion = Announcement.objects.filter(course=icourse)
		discussion_list.extend(course_discussion)
		
		
#professor makes announcement
def make_announcement(request):
	courses = Course.objects.filter(students__username=request.user.username)
	return render_to_response('make_announcement.html',
	{'courses': courses},
	context_instance=RequestContext(request))


