from django.shortcuts import render_to_response
from models import Assignment

def assignments(request):
    list_of_assignments = Assignment.objects.all()
    return render_to_response('assignments.html', {
        'list_assignments': list_of_assignments,
    })