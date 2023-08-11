from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True) 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    salary = models.IntegerField(default=0)
    task = models.CharField(max_length=100)
    workinprog = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    phone = PhoneNumberField(blank=True)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
