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

