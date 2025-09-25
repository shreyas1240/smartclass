from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name  = models.CharField(max_length=100)
    roll_no    = models.CharField(max_length=30)
    course     = models.CharField(max_length=50, blank=True)
    fees_due   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    attendance = models.PositiveIntegerField(default=0)  # percentage or count

    def __str__(self):
        return self.full_name
