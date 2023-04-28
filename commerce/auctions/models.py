from django.contrib.auth.models import AbstractUser
from django.db import models

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    currentPrice = models.FloatField()
    image = models.ImageField(upload_to='images/', default='images/None/no-img.jpg')
    
    def __str__(self):
        return f"{self.id}. {self.title}, ${self.currentPrice}"
    
    
class User(AbstractUser):
    testText = models.CharField(max_length=64, default="test")
    
