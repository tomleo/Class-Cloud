from django.db import models
from django.contrib.auth.models import User

class TimeStampedActivate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Assignment(TimeStampedActivate):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, related_name="assignments")

    def __unicode__(self):
        return self.name
