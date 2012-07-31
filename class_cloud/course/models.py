import datetime
import os.path
from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from django.contrib.admin import widgets

from django.template.defaultfilters import slugify


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


class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ('points', 'max_points')


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

#Remove or move this?
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description', 'syllabus', 'course_image')

class AssignmentAttempt(models.Model):
    attachment = models.FileField(upload_to='assignment_submissions')
    comments = models.TextField(blank=True)
    submit_date = models.DateTimeField(auto_now_add=True, blank=True)


class Assignment(TimeStampedActivate):
    """
    An assignment represents a homework assignment or task.
    Assignments have an assosiated User and course
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(default=False)

    teacher = models.ForeignKey(User, related_name="assignments")
    course = models.ForeignKey(Course, related_name="classes")
    attachments = models.FileField(upload_to='assignment_attachments', blank=True)
    
    objects = AssignmentManager() #What does this do? Maybe i should remove this
    
    grade = models.ManyToManyField(Grade, through='StudentGrade')
    submissions = models.ManyToManyField(AssignmentAttempt, through='SubmittedAssignment')
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Assignment, self).save(*args, **kwargs)
    
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

#via http://strattonbrazil.blogspot.com/2011/03/using-jquery-uis-date-picker-on-all.html
def make_custom_datefield(f):
    formfield = f.formfield()
    if isinstance(f, models.DateField):
        formfield.widget.format = '%m/%d/%Y'
        formfield.widget.attrs.update({'class':'datePicker', 'readonly':'true'})
    return formfield


class AssignmentForm(ModelForm):
    formfield_callback = make_custom_datefield
    active = forms.BooleanField(label='Make Visible to Students')
    class Meta:
        model = Assignment
        fields = ('name', 'description', 'due_date', 'attachments', 'active')
        #widgets = {
        #    'attachments': AdminFileWidget()
        #}


class SubmittedAssignment(models.Model):
    student = models.ForeignKey(User, verbose_name="Student")
    assignment = models.ForeignKey(Assignment, verbose_name="Assignment")
    submission = models.ForeignKey(AssignmentAttempt)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #Additional fields will go here
    

class StudentGrade(models.Model):
    student = models.ForeignKey(User, verbose_name="Student")
    assignment = models.ForeignKey(Assignment, verbose_name="For Assignment")
    grade = models.ForeignKey(Grade, verbose_name="Students Grade")
    
class StudentGradeForm(ModelForm):
    class Meta:
        model = StudentGrade

class Enrollment(models.Model):
    #Should change this to student...
    students = models.ForeignKey(User, 
                                 verbose_name="Enrolled",
                                 help_text="Enroll this user as student in Course."
                                 )
    course = models.ForeignKey(Course, verbose_name="In Course",)
    start_date = models.DateField()


class Announcement(TimeStampedActivate):
    title = models.CharField(max_length = 255)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)
    course = models.ForeignKey(Course, related_name ="class")
    teacher = models.ForeignKey(User, related_name="announcements")

    def __unicode__(self):
	    return self.description

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Announcement, self).save(*args, **kwargs)

class AnnoucementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'description')


class Discussion(TimeStampedActivate):
	disqus = models.TextField(blank = True, help_text = "disqus")
	slug = models.SlugField()
	pub_date = models.DateTimeField('date published')
	course = models.ForeignKey(Course, related_name = "course")
	user = models.ForeignKey(User, related_name = "user")
	
	def __unicode__(self):
		return self.slug


	
