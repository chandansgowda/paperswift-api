from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from paperswift_api import settings

# Create your models here.

class Department(models.Model):
    code = models.CharField(max_length=50,primary_key=True)
    name = models.CharField(max_length=255)
    hod = models.OneToOneField('Teacher', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.dept_short_name


class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_external = models.BooleanField(default=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    mobile_no = models.CharField(max_length=15)
    address = models.TextField()
    designation = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    bank_account_no = models.CharField(max_length=20)
    bank_ifsc = models.CharField(max_length=15)
    bank_name = models.CharField(max_length=255)
    pan_no = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.name} - {self.designation}"


class Scheme(models.Model):
    sid = models.AutoField(primary_key=True)
    year = models.IntegerField()
    guidelines_doc_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.year} Scheme"


class Course(models.Model):
    """
    Course Details
    """
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255, null=False)
    scheme = models.ForeignKey('Scheme', on_delete=models.CASCADE)
    syllabus_doc_url = models.URLField(null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    sem = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.code})"


class Examination(models.Model):
    """
    Examination details to which papers are being set.
    """
    eid = models.AutoField(primary_key=True)
    sem = models.IntegerField()
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    is_supplementary = models.BooleanField(default=False)
    paper_submission_deadline = models.DateField()

    def __str__(self):
        return f"{self.sem} Sem Exam {'SUP' if self.isSupplementary else ''}"


class AssignmentStatus(models.TextChoices):
    REQUEST_PENDING = 'Request Pending', _('Request Pending')
    IN_PROGRESS = 'In Progress', _('In Progress')
    UPDATE_REQUESTED = 'Update Requested', _('Update Requested')
    COMPLETED = 'Completed', _('Completed')


class Assignment(models.Model):
    """
    Details on who is assigned to which course.
    """
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paper_setter = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.REQUEST_PENDING,
    )
    submission_date = models.DateTimeField(null=True, blank=True)
    qp_doc_url = models.URLField(null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    payment_ref_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.course} - {self.paper_setter}"


class SuggestedPaperSetter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paper_setter = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE, null=True)
    isExternal = models.BooleanField(default=True)