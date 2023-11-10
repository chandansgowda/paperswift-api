from datetime import timezone
from django.db import models

# Create your models here.

class PaperSetter(models.Model):
    """
    Paper Setter Details
    """
    psid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)

class Course(models.Model):
    """
    Course Details
    """
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    scheme = models.IntegerField()

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
    paper_setter = models.ForeignKey(PaperSetter, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.REQUEST_PENDING,
    )
