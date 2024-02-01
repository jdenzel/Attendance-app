from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TimeClock(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    clock_in_time = models.DateTimeField(auto_now_add=True)
    clock_out_time = models.DateTimeField(auto_now_add=True)

    