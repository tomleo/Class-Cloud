from django.shortcuts import render_to_response
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
