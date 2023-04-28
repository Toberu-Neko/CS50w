from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
class User(AbstractUser):
    pass

categoryKeys = [('1',"None"), ('2',"Fasion"), ("3","Toys"), ("4","Electronics"), ("5","Home"), ("6","Other")]
class Listing(models.Model):
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=1, choices=categoryKeys)
    description = models.CharField(max_length=64)
    
    startPrice = models.FloatField(validators=[MinValueValidator(0.1)])
    currentPrice = models.FloatField(validators=[MinValueValidator(0.1)], default=startPrice)
    
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='images/', default='images/None/NoImage.png')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}. {self.title}, ${self.currentPrice}"

class Bids(models.Model):
    pass

class Comments(models.Model):
    comment = models.CharField(max_length=64)
    

    
