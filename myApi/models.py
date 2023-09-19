from django.db import models

# Create your models here.

class Employee(models.Model):
    firstname=models.CharField(max_length=200)
    lastname = models.CharField(max_length=200, default='')
    email=models.CharField(max_length=200)
    phone = models.IntegerField(max_length=12, default=0)
    message=models.CharField(max_length=200)
    


    def __str__(self):
        return self.firstname