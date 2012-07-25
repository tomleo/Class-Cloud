from django import forms

class AddCourse(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.TextField()
    syllabus = forms.FileField()
    course_image = forms.ImageField()
    
     title = models.CharField(max_length=255, help_text="Name of course")
    slug = models.SlugField()
    description = models.TextField(blank=True,
                                    help_text="Course Description.")
    #urls.py controlls what is served up to a user so the path you store
    #pictures in isn't accessable to the user.
    #syllabus = models.FileField(upload_to='{0}/syllabus'.format(getFilePath()))
    #syllabus = models.FileField(upload_to='syllabus')
    #course_image = models.ImageField(upload_to = 'course_image')
    teacher = models.ForeignKey(User, related_name="courses")
    #students = models.ManyToManyField(User, through='Enrollment', blank=True)

