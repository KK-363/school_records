from pyexpat import model
from django.db import models
from students.models import Student

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250, blank=False, default='')
    extra_curricular = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Subject_Student(models.Model):
    students = models.ManyToManyField(Student)