from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TimeClock(models.Model):
    ROLES = [
        ('scoreboard', 'Scoreboard'),
        ('paperscorer', 'Paper Scorer'),
        ('camera', 'Camera Operator'),
        ('onlinescorer', 'Online Scorer'),
        ('gamechange', 'Game Changer'),
        ('subtime', 'Sub timer'),

    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    clock_in_time = models.DateTimeField(auto_now_add=True)
    clock_out_time = models.DateTimeField(auto_now_add=True)
    role = models.CharField(choices = ROLES, default='none')

    def __str__(self):
        return self.employee + '\n' + self.date + self.clock_in_time + '\n' + self.clock_out_time + '\n' + self.role 

    