from django.db import models
from django.contrib.auth.models import User
import datetime


def getFilePath():
    theDate = datetime.datetime.now()
    y = theDate.year
    m = theDate.month
    d = theDate.day
    return '{year}/{month}/{day}'.format(year=y, month=m, day=d)


class TimeStampedActivate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=False)
    end_date = models.DateTimeField(default=False)

    class Meta:
        abstract = True


class Teacher(User):
    """
    A course has a teacher
    which is a specific type of User
    """

    def __unicode__(self):
        return self.email


class Student(User):
    """
    A course has many students,
    a student is a specific type of User
    """

    def __unicode__(self):
        return self.email


class Course(TimeStampedActivate):
    title = models.CharField(max_length=255,
                            help_text="Name of course")
    description = models.TextField(blank=True,
                                    help_text="Course Description.")
    #urls.py controlls what is served up to a user so the path you store
    #pictures in isn't accessable to the user.
    #syllabus = models.FileField(upload_to='{0}/syllabus'.format(getFilePath()))
    syllabus = models.FileField(upload_to='syllabus')

    def __unicode__(self):
        return '{0}'.format(self.title)


class Grade(models.Model):
    letter_grade = models.CharField(max_length=2,
                                    help_text="Letter grade A, B, C, D, or F")


class Assignment(TimeStampedActivate):
    name = models.CharField(max_length=255,
                            help_text="Name of assignment.")
    description = models.TextField(blank=True,
                                    help_text="Describe the assignment.")
    user = models.ForeignKey(User, related_name="assignments")
    assignment_grade = models.ForeignKey(Grade)

    def __unicode__(self):
        return self.name
