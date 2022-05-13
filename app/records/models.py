from django.db import models
from django.utils import timezone
from subjects.models import Subject_Student


# Create your models here.
class Record(models.Model):
    date = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    time_spent = models.DecimalField(max_digits=10, decimal_places=2)
    subject_student = models.ForeignKey(Subject_Student, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.date