import datetime

from django.db import models
from django.contrib.auth.models import User


class TimeStamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class TimeStampedActivate(TimeStamped):
    active = models.BooleanField(default=False)
    #start_date = models.DateTimeField(default=False)
    

    class Meta:
        get_latest_by = 'due_date'
        ordering = ('-modified', '-created',)
        abstract = True


class AssignmentManager(models.Manager):
    def get_visible(self):
        # look into filter option
        # end_date__lte=datetime.datetime.now()
        return self.get_query_set().filter(active=True)
        

class Course(TimeStampedActivate):
    """
    A Course represents a academic course that a student
    might enrole in.
    """
    title = models.CharField(max_length=255,
                            help_text="Name of course")
    slug = models.SlugField()
    description = models.TextField(blank=True,
                                    help_text="Course Description.")
    #urls.py controlls what is served up to a user so the path you store
    #pictures in isn't accessable to the user.
    #syllabus = models.FileField(upload_to='{0}/syllabus'.format(getFilePath()))
    syllabus = models.FileField(upload_to='syllabus')
    user = models.ForeignKey(User, related_name="courses")

    def __unicode__(self):
        return '{0}'.format(self.title)

    class Meta:
        ordering = ["-title"]

    @models.permalink
    def get_absolute_url(self):
        return ('course', (), {
            'slug': self.slug
        })


class Assignment(TimeStampedActivate):
    """
    An assignment represents a homework assignment or task.
    Assignments have an assosiated User and course
    """
    name = models.CharField(max_length=255,
                            help_text="Name of assignment.")
    slug = models.SlugField()
    description = models.TextField(blank=True,
                                    help_text="Describe the assignment.")
    #May want to change this relationship, so that assignments
    #have a OneToMany relationship with Student?
    due_date = models.DateTimeField(default=False)
    user = models.ForeignKey(User, related_name="assignments")
    course = models.ForeignKey(Course, related_name="classes")
    
    objects = AssignmentManager()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('assignment', (), {
            'course': self.course.slug,
            'slug': self.slug
        })

    class Meta:
        ordering = ['-due_date', '-modified', '-created']


###
#Stuff to be modified after the prototype
###

class Grade(models.Model):
    """
    Note sure how to implement this, I think that this should be a
    foreignkey on Student, as teachers don't get grades.

    Alternativly It should somehow relate to an Assignment, and
    a course as a whole.

    Students have course grades, Students have assignment grades
    """
    letter_grade = models.CharField(max_length=2,
                                    help_text="Letter grade A, B, C, D, or F")


class Person(TimeStamped):
    """
    A Person is a User with the following attributes
    """
    first_name = models.CharField(verbose_name="First Name", max_length=60)
    last_name = models.CharField(verbose_name="Last Name", max_length=60)
    email = models.EmailField(verbose_name="Email Address")
    user = models.ForeignKey(User,unique=True,verbose_name="User",blank=True,null=True)

    def full_name(self):
        return '{fname} {lname}'.format(fname=first_name,
                                        lname=last_name)

    def __unicode__(self):
        return self.full_name()

    class Meta:
        verbose_name_plural = "People"

    @models.permalink
    def get_absolute_url(self):
        pass

class Teacher(Person):
    """
    A course has a teacher
    which is a specific type of Person
    """
    courses = models.ManyToManyField('Course')

    def __unicode__(self):
        return self.email


class Student(Person):
    """
    A course has many students,
    a student is a specific type of Person
    """

    def __unicode__(self):
        return self.email

class Enrollment(models.Model):
    student = models.ForeignKey(Student,
                                verbose_name="Enrolled",
                                help_text="Enroll this user as student in Course.",
                                )
    course = models.ForeignKey(Course,
                                verbose_name="In Course",)
    start_date = models.DateField()
