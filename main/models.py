from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Oculi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    amount_collected = models.IntegerField()
    amount = models.IntegerField()
    description = models.TextField()