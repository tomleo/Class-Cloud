import datetime

from django.db import models
from django.contrib.auth.models import User


class TimeStamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class TimeStampedActivate(TimeStamped):
    active = models.BooleanField(default=False)

    class Meta:
        get_latest_by = 'due_date'
        ordering = ('-modified', '-created',)
        abstract = True


#wtf what does this do?
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
    teacher = models.ForeignKey(User, related_name="courses")
    students = models.ManyToManyField(User, through='Enrollment', blank=True)

    def __unicode__(self):
        return '{0}'.format(self.title)

    class Meta:
        ordering = ["-title"]
        permissions = (
            ('view_course', 'This course is visible'),
            ('edit_course', 'This course can be modified'),
        )

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

    #Not sure user makes sense here
    #todo - maybe remove the user foreignkey
    teacher = models.ForeignKey(User, related_name="assignments")
    course = models.ForeignKey(Course, related_name="classes")
    objects = AssignmentManager() #What does this do?

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


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #Additional fields will go here


class Grade(models.Model):
    """
    Note sure how to implement this, I think that this should be a
    foreignkey on Student, as teachers don't get grades.

    Alternativly It should somehow relate to an Assignment, and
    a course as a whole.

    Students have course grades, Students have assignment grades
    """
    letter_grade = models.CharField(max_length=10,
                                    help_text="Letter grade A, B, C, D, or F")
    course = models.ForeignKey(Course)
    assignment = models.ForeignKey(Assignment)
    
    def __unicode__(self):
        return self.letter_grade

class Enrollment(models.Model):
    #student = models.ForeignKey(Student,
    #                            verbose_name="Enrolled",
    #                            help_text="Enroll this user as student in Course.",
    #                            )
    students = models.ForeignKey(User, 
                                 verbose_name="Enrolled",
                                 help_text="Enroll this user as student in Course."
                                 )
    course = models.ForeignKey(Course,
                                verbose_name="In Course",)
    start_date = models.DateField()

