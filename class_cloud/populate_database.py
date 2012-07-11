import datetime
from course.models import Assignment, Grade, Course, User

bob = User.objects.create_user('bob', 'bob@localhost', 'thomas')
bob.save()

course1  = Course(title="course 1", slug="course-1", description="description", user=bob)
course1.save()

week_from_today = datetime.timedelta(days=7)
sample_due_date = datetime.date.today() + week_from_today
assignment1 = Assignment(name="assignment 1",
                         slug="assignment-1",
                         description="Assignment 1 description",
                         #due_date=datetime.datetime(2012, 7, 31, 5, 0, tzinfo=<UTC>),
                         due_date=sample_due_date,
                         user=bob,
                         course=course1)
assignment1.save()

grade1 = Grade(letter_grade="A",course=course1,assignment=assignment1)
grade1.save()


