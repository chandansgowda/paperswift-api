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

class Assignment(models.Model):
    """
    Details on who is assigned to which course.
    """
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    paper_setter = models.OneToOneField(PaperSetter, on_delete=models.CASCADE)
    hasAgreed = models.BooleanField(default=False)
    isFinalized = models.BooleanField(default=False)
