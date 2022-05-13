from django.db import models

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    grade = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        name = self.first_name + " " + self.last_name
        return name