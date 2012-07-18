import datetime
import os.path
from django.db import models
from django.contrib.auth.models import User

"""
TimeStamped
TimeStampedActivate

Grade

Course
Assignment

StudentGrade
Enrollment

AssignmentManager
UserProfile
"""

class TimeStamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class TimeStampedActivate(TimeStamped):
    active = models.BooleanField(default=False)

    class Meta:
        get_latest_by = 'due_date'
        ordering = ('-modified', '-created',)
        abstract = True


class Grade(models.Model):
    points = models.IntegerField()
    max_points = models.IntegerField()

    def calculate_grade(self):
        return int(((float(self.points))/float(self.max_points)) * 100)


    def letter_grade(self):
        g = self.calculate_grade()
        if   g>=90: return 'A'
        elif g>=80: return 'B'
        elif g>=70: return 'C'
        elif g>=60: return 'D'
        else: return 'F'


    def __unicode__(self):
        return self.letter_grade()


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
    title = models.CharField(max_length=255, help_text="Name of course")
    slug = models.SlugField()
    description = models.TextField(blank=True,
                                    help_text="Course Description.")
    #urls.py controlls what is served up to a user so the path you store
    #pictures in isn't accessable to the user.
    #syllabus = models.FileField(upload_to='{0}/syllabus'.format(getFilePath()))
    syllabus = models.FileField(upload_to='syllabus')
    course_image = models.ImageField(upload_to = 'course_image')
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
    
    grade = models.ManyToManyField(Grade, through='StudentGrade')
    
    attachments = models.FileField(upload_to='assignment_attachments', blank=True)
    
    objects = AssignmentManager() #What does this do? Maybe i should remove this
    
    def filename(self):
        return os.path.basename(self.attachments.name)
    
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
    

class StudentGrade(models.Model):
    student = models.ForeignKey(User, verbose_name="Student")
    assignment = models.ForeignKey(Assignment, verbose_name="For Assignment")
    grade = models.ForeignKey(Grade, verbose_name="Students Grade")





class Enrollment(models.Model):
    students = models.ForeignKey(User, 
                                 verbose_name="Enrolled",
                                 help_text="Enroll this user as student in Course."
                                 )
    course = models.ForeignKey(Course, verbose_name="In Course",)
    start_date = models.DateField()

