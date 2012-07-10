import datetime

from django.core.management import setup_environ
import settings
setup_environ(settings)

from course.models import Assignment, Grade, Course, User

#course = Course.objects.get(slug='course-1')
#assignment = Assignment.objects.filter(course=course)
#grade = Grade.objects.filter(course=course, assignment=assignment[1])

#Create a user
bob = User.objects.create_user('bob', 'bob@localhost', 'thomas')
bob.save()

course1  = Course(title="course 1", slug="course-1", description="description", user=bob)
course1.save()

assignment1 = Assignment(name="assignment 1", slug="assignment-1", description="Assignment 1 description", due_date=datetime.datetime(2012, 7, 31, 5, 0, tzinfo=<UTC>), user=bob, course=course1)
assignment1.save()

