from django.db import models

# Create your models here.
class Test(models.Model):
    attribute = models.CharField(max_length=50)
