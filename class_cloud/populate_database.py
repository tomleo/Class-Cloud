import datetime
from course.models import Assignment, Grade, Course, User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

student_users = Group(name='Student Users')
teacher_users = Group(name='Teacher Users')
ct = ContentType.objects.get(app_label='course', model='course')
student_view = Permission(name='Student View', 
                          codename='student_view',
                          content_type=ct)
student_view.save()
teacher_view = Permission(name='Teacher View',
                          codename='teacher_view',
                          content_type=ct)
teacher_view.save()
student_users.permissions.add(student_view)
teacher_users.permissions.add(teacher_view)
student_users.save()
teacher_users.save()

bob = User.objects.create_user('bob', 'bob@bob.com', 'thomas')
bob.groups.add(student_users)
bob.save()

durga = User.objects.create_user('durga', 'durga@durga.com', 'thomas')
durga.groups.add(teacher_users)
durga.save()

course1  = Course(title="course 1", slug="course-1", description="description", teacher=bob)
course1.save()

week_from_today = datetime.timedelta(days=7)
sample_due_date = datetime.date.today() + week_from_today
assignment1 = Assignment(name="assignment 1",
                         slug="assignment-1",
                         description="Assignment 1 description",
                         #due_date=datetime.datetime(2012, 7, 31, 5, 0, tzinfo=<UTC>),
                         due_date=sample_due_date,
                         teacher=bob,
                         course=course1)
assignment1.save()

grade1 = Grade(letter_grade="A",course=course1,assignment=assignment1)
grade1.save()








