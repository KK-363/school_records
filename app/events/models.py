from django.db import models
import datetime
from students.models import Student
from subjects.models import Subject


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date.today)
    start_time = models.TimeField()
    event_length = models.DecimalField(max_digits=10, decimal_places=2)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name