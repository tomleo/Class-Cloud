#Don't think generic views are being used, might want to remove this
from django.views.generic import list_detail, date_based, TemplateView, RedirectView, DetailView
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt


#Models
from course.models import Course, Assignment, Grade, StudentGrade, SubmittedAssignment, Announcement, Discussion, Enrollment, AssignmentAttempt
from django.contrib.auth.models import User, Permission

#Model Forms
from course.models import CourseForm, AnnoucementForm, AssignmentForm, GradeForm, AssignmentAttemptForm
from django.forms.models import ModelForm, modelformset_factory

from django.shortcuts import render_to_response, RequestContext

from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.urlresolvers import reverse

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from django.template import defaultfilters

def calendar(request):
    assignment_list = []
    courses = []
    courses.extend(Course.objects.filter(students__username=request.user.username))
    
    for icourse in courses:
        course_assignments = Assignment.objects.filter(course=icourse)
        assignment_list.extend(course_assignments)

    return render_to_response('calendar.html',
    		{'assignments': assignment_list},
        	context_instance=RequestContext(request))


def passign(request):
    return render_to_response('passign.html',
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
def profile(request):
	name = request.user
	courses = Course.objects.filter(students__username=request.user.username)
	return render_to_response('profile.html',
	{'name': name,
	 'courses': courses,},
	context_instance=RequestContext(request))

def course_test(request, course_slug):
    
    selected_course = Course.objects.get(slug=course_slug)
    course_assignments = Assignment.objects.filter(course=selected_course)
    
    import pdb; pdb.set_trace()
    
    return HttpResponse(course_assignments)


#@login_required
#@user_passes_test(lambda u: u.has_perm('course.student_view'))
#def wtf(request):
#    student_grades = StudentGrade.objects.filter(student__username=request.user.username)
#    return render_to_response('grades.html',
#        {'student_grades': student_grades},
#        context_instance=RequestContext(request))
    
@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def course_grades(request, course_slug):    
    
    selected_course = Course.objects.get(slug=course_slug)
    
    # all grades associated with given course and user
    student_grades = StudentGrade.objects.filter(student__username=request.user.username,
                                          assignment__course=selected_course) 

    submitted = SubmittedAssignment.objects.filter(student__username=request.user.username)
    
    a_graded = []
    a_submitted = []
   
    for submission in submitted:
        for student_grade in student_grades:
            if submission.assignment == student_grade.assignment:
                a_graded.append((student_grade.grade, submission))
                                          
    template_name = 'course_grades.html'
    return render_to_response(template_name, 
        {'course':selected_course,
         'assignments_graded':a_graded,
         'grades':student_grades},
         context_instance=RequestContext (request))                                      

@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def grades(request):
    
    grades = {}
    
    #Filter student grades by the students enrolled courses
    enrolled = Enrollment.objects.filter(students__username=request.user.username)
    student_grades = StudentGrade.objects.filter(student__username=request.user.username)

    for grade in student_grades:
        if grade.assignment.course in [e.course for e in enrolled]:
            if grade.assignment.course.title not in grades:
                grades[grade.assignment.course.title] = [grade]
            else:
                grades[grade.assignment.course.title].append(grade)

    return render_to_response('grades.html',
        {'student_grades': grades},
        context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def course(request, course_slug):
    selected_course = Course.objects.get(slug=course_slug)

    # Need to further filter this by due dates and wheather the assignment is active
    course_assignments = Assignment.objects.filter(course=selected_course)
    
    course_announcements = Announcement.objects.filter(course = selected_course)
    course_discussions = Discussion.objects.filter(course = selected_course)
    
    submitted = SubmittedAssignment.objects.filter(student__username=request.user.username)
    
    # all grades associated with given course and user
    student_grades = StudentGrade.objects.filter(student__username=request.user.username,
                                          assignment__course=selected_course)

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
         },
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

#We need to filter those assignments out that are past due, submitted or graded.
#ToDo
#best of luck
       
@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def assignment(request, slug):

    a = Assignment.objects.get(slug=slug)
    b = a.course
    return render_to_response('assignment.html',
        {'assignment':a,
         'course':b,},
        context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def course_assignment(request, course_slug, assignment_slug):
    a = Assignment.objects.get(slug=assignment_slug)
    b = a.course
    
    user = request.user
    graded_submissions = StudentGrade.objects.filter(assignment__slug=assignment_slug, student=user)
    submissions = SubmittedAssignment.objects.filter(assignment__slug=assignment_slug, student=user)
    
    if graded_submissions:
        submission_status = "graded"
    elif submissions:
        submission_status = "submitted"
    else:
        submission_status = "need to submit"
    
    template_vars = {
        'assignment': a,
        'course': b,
        'submission_status': submission_status
    }

    return render_to_response('assignment.html',
        template_vars,
        context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm('course.student_view'))
def course_assignment_edit(request, course_slug, assignment_slug):
    """
    Edit Assignment Submission if it hasn't been graded yet

    Not yet functional, will not be implemented for seniorr design showcase
    """
    submissionAssignment = SubmittedAssignment.objects.filter(student=request.user, assignment__slug=assignment_slug)
    EditAssignmentSubmissionForm = modelformset_factory(SubmittedAssignment, max_num=1, extra=0)
    if request.method == 'POST':
        formset = EditAssignmentSubmissionForm(request.POST, request.FILES,
                                               queryset=SubmittedAssignment.objects.filter(student=request.user,
                                                   assignment__slug=assignment_slug))
        if formset.is_valid():
            instance = formset.save(commit=False)
            for instance in instances:
                instance.save()
            return HttpResponseRedirect("complete/")
    else:
        formset = EditAssignmentSubmissionForm(queryset=SubmittedAssignment.objects.filter(student=request.user,
                                                   assignment__slug=assignment_slug))
    return render_to_response('assignment_complete.html',
        {'formset': formset},
        context_instance=RequestContext(request))

    
    
def course_assignment_submit(request, course_slug, assignment_slug):
    assignment = Assignment.objects.get(slug=assignment_slug)
    submission = AssignmentAttempt()
    #courses/(?P<course_slug>[-\w]+)/(?P<assignment_slug>[-\w]+)/complete/

    if request.method == 'POST':
        form = AssignmentAttemptForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            submission = form.save()
            full = SubmittedAssignment(student=request.user, assignment=assignment, submission=submission)
            full.save()
            return HttpResponseRedirect('complete/')
    else:
        form = AssignmentAttemptForm()

    return render_to_response('assignment_submit.html',
            {'form':form},
            context_instance=RequestContext(request))

    
def course_assignment_complete(request, course_slug, assignment_slug):

    #request.META['HTTP_REFERER'] = http://localhost:8000/courses/course-2/hope-this-works/submit/
    cf = request.META['HTTP_REFERER']
    comingFrom = cf.split('/')[-2]
    #are you coming from...
    #if comingFrom is 'submit':
    #    pass
    #elif comingFrom is 'edit':
    #    pass
    #else:
    #    pass

    return render_to_response('assignment_complete.html',
            {'course_slug': course_slug,
             'assignment_slug': assignment_slug,
             'comingFrom':comingFrom },
            context_instance=RequestContext(request))

def course_assignment_grade(request, course_slug, assignment_slug):

    #at the moment I am only grabbing the first grade in the list,
    #for later iterations it might be interesting to re-submit an assignment and
    #see all versions submitted
    sg = StudentGrade.objects.filter(assignment__slug=assignment_slug, student=request.user)

    #grade = sg[0].grade

    sub = SubmittedAssignment.objects.filter(student=request.user, assignment__slug=assignment_slug)
    #sub is returning an empty list, if the course has a grade then it should
    #have also been submitted... 
    #import pdb; pdb.set_trace()

    submission = sub[0].submission

    return render_to_response('assignment_grade.html',
        {'studentgrade': sg[0],
         'submission': submission},
        context_instance=RequestContext(request))

def course_assignment_view(request, course_slug, assignment_slug):
    assignment = Assignment.objects.get(slug=assignment_slug)
    sub = SubmittedAssignment.objects.filter(student=request.user, assignment__slug=assignment_slug)

    return render_to_response('assignment_view.html',
            {'assignment': assignment,
             'submission': sub[0].submission},
            context_instance=RequestContext(request))


def logout_view(request):
    logout(request)


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
		

## TEACHER VIEWS ##

@login_required
@user_passes_test(lambda u: u.has_perm('course.teacher_view'))
def teacher_index(request):
    courses = Course.objects.filter(teacher=request.user)
    teacher = request.user.get_full_name()
    #import pdb; pdb.set_trace()
    return render_to_response('teacher/index.html',
        {'teacher': teacher,
         'courses': courses },
        context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm('course.teacher_view'))
def teacher_course(request, course_slug):
    
    course = Course.objects.get(slug=course_slug)
    courses = Course.objects.filter(teacher=request.user)	
    return render_to_response('teacher/course.html',
        { 'course': course,
          'courses': courses, },
        context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm('course.teacher_view'))
def annoucement_add(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    courses = Course.objects.filter(teacher=request.user)
    annoucement = Announcement(course=course, teacher=course.teacher)
    
    if request.method == 'POST':
        form = AnnoucementForm(request.POST, instance=annoucement)
        if form.is_valid():
            annoucement = form.save()
            return HttpResponseRedirect("/teacher/{0}/annoucement_complete/".format(course.slug))
    else:
        form = AnnoucementForm()
    
    return render_to_response('teacher/annoucement_add.html',
        { 'announcementForm': form, 
        'course':course,
        'courses':courses,},
        context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm('course.teacher_view'))
def annoucement_complete(request, course_slug):
    return render_to_response('teacher/annoucement_complete.html',
        {'slug':course_slug},
        context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm('course.teacher_view'))
def assignment_add(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    courses = Course.objects.filter(teacher=request.user)
    assignment = Assignment(course=course, teacher=course.teacher)
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            assignment = form.save()
            return HttpResponseRedirect("/teacher/{0}/assignment_complete/".format(course.slug))
    else:
        form = AssignmentForm()
    
    return render_to_response('teacher/assignment_add.html',
        { 'assignmentForm': form,
          'course':course,
          'courses':courses,},
        context_instance=RequestContext(request))
        

@login_required
@user_passes_test(lambda u: u.has_perm('course.teacher_view'))
def assignment_complete(request, course_slug):
    return render_to_response('teacher/assignment_complete.html',
        {'slug':course_slug},
        context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm('course.teacher_view'))
def grade_assignments(request, course_slug):

    course = Course.objects.get(slug=course_slug)
    courses = Course.objects.filter(teacher=request.user)

    course_assignments = Assignment.objects.filter(course=course)

    submitted = SubmittedAssignment.objects.filter(assignment__course=course)

    assignments = {}

    for assignment in course_assignments:
        assignments[assignment.name] = []
        for submission in submitted:
            if submission.assignment.name == assignment.name:
                assignments[assignment.name].append(submission)
                #submitted.remove(submission) #This will speed things up a little?

    return render_to_response('teacher/grade_assignments.html',
        {'assignments': assignments,
         'course':course,
         'courses':courses, },
        context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm('course.teacher_view'))
def grade_assignment(request, course_slug, assignment_slug, student_username):

    #student & assignment
    courses = Course.objects.filter(teacher=request.user)
    assignment = Assignment.objects.get(slug=assignment_slug)
    student = User.objects.get(username=student_username)
    
    grade = Grade()
    student_grade = StudentGrade(student=student, assignment=assignment)

    #GradeForm
    #StudentGradeForm

    #course = Course.objects.get(slug=course_slug)
    #assignment = Assignment(course=course, teacher=course.teacher)
    
    if request.method == 'POST':
        form = GradeForm(request.POST, request.FILES, instance=grade)
        if form.is_valid():
            grade = form.save()
            student_grade.grade = grade
            student_grade.save()
            return HttpResponseRedirect("/teacher/{0}/grade_assignments/{1}/{2}/assignment_graded/".format(course_slug, assignment_slug, student_username))
    else:
        form = GradeForm()


    return render_to_response('teacher/grade_assignment.html',
        {'form': form,
        'courses':courses,},
        context_instance=RequestContext(request))
    
    
@login_required
@user_passes_test(lambda u: u.has_perm('course.teacher_view'))
def grade_assignment_complete(request, course_slug, assignment_slug, student_username):
    return render_to_response('teacher/grade_assignment_complete.html',
        {'slug': course_slug},
        context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.has_perm('course.teacher_view'))
def edit_course(request, course_slug):

    EditCourseFormSet = modelformset_factory(Course, max_num=1, extra=0,)
    if request.method == 'POST':
        formset = EditCourseFormSet(request.POST, request.FILES, 
                                    queryset=Course.objects.filter(slug=course_slug))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                #instance.save_m2m()
                instance.save()
            return HttpResponseRedirect("/teacher/")
    else:
        formset = EditCourseFormSet(queryset=Course.objects.filter(slug=course_slug))

    return render_to_response('teacher/edit_course.html',
        {'formset': formset},
        context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.has_perm('course.teacher_view'))
def edit_course_complete(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    return render_to_response('teacher/edit_course_complete.html',
        {'slug': course_slug},
        context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.has_perm('course.teacher_view'))
def enroll_students(request, course_slug):
    """
    get all students that are not teachers, and not enrolled in course
    """
    courses = Course.objects.filter(teacher=request.user)    
    course = Course.objects.get(slug=course_slug)
    student_permission = Permission.objects.get(codename='student_view')
    #students = User.objects.filter(Q(groups__permissions=student_permission) | Q(user_permissions=student_permission)).distinct()

    
    #All Enrollments or the class
    enrollments = Enrollment.objects.filter(course=course)

    allStudents = [i.students for i in enrollments]
    not_enrolled = [enrolled.course!=course for enrolled in enrollments]
    
    return render_to_response('teacher/enroll_students.html',
            {'enrolled_students': allStudents,
             'not_enrooled_students': not_enrolled,
             'course':course,
             'courses':courses, },
            context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.has_perm('course.teacher_view'))
def enroll_student(request, course_slug, student):
    """
    create submissioin form to enroll student
    """
    pass

@login_required
@user_passes_test(lambda u: u.has_perm('course.teacher_view'))
def enroll_student_complete(request, course_slug):
    pass

#@login_required
#@user_passes_test(lambda u: u.has_perm('course.teacher_view'))
#def teacher_enroll(request):
#    """Enroll Student in class"""
#    pass


@login_required
@user_passes_test(lambda u: u.has_perm('course.teacher_view'))    
def add_course(request):
    pass



