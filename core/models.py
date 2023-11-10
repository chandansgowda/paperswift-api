from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from paperswift_api import settings

# Create your models here.


class Course(models.Model):
    """
    Course Details
    """
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255, null=False)
    scheme = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.code})"


class AssignmentStatus(models.TextChoices):
    REQUEST_PENDING = 'Request Pending', _('Request Pending')
    IN_PROGRESS = 'In Progress', _('In Progress')
    UPDATE_REQUESTED = 'Update Requested', _('Update Requested')
    COMPLETED = 'Completed', _('Completed')


class Assignment(models.Model):
    """
    Details on who is assigned to which course.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paper_setter = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.REQUEST_PENDING,
    )
