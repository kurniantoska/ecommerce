from django.db import models

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(default='description default text')
    location = models.CharField(max_length=123, default='my location default')
    job = models.CharField(max_length=120, null=True)

    def __str__(self):
        return self.name