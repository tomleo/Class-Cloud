import datetime
from course.models import Assignment, Grade, Course, User

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


bob = User.objects.create_user('bob', 'bob@localhost', 'thomas')
bob.save()

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

student_users = Group(name='Student Users')
student_users.save()
teacher_users = Group(name='Teacher Users')
teacher_users.save()

#This does not work, need to find a way to progrmatically create groups for users
#Alternativly maybe permissions should be via the models meta data
student_view_ct = Course.objects.get(app_label='course', model='Course', name='Course Type')
can_view = Permission(name='Can View',
                      codename='student',
                      content_type=student_view_ct)
can_view.save()
can_modify = Permission(name='Can Modify',
                        codename='teacher',
                        content_type=student_view_ct)
can_modify.save()





