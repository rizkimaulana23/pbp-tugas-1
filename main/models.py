from django.db import models

# Create your models here.
class Oculi(models.Model):
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    amount_collected = models.IntegerField()
    amount = models.IntegerField()
    description = models.TextField()