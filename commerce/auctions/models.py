from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
class User(AbstractUser):
    watchList = models.ManyToManyField('Listing', blank=True, related_name="watchList")
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
    # bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder", null=True, blank=True)
    bids = models.ManyToManyField('Bids', blank=True, related_name='listing_bids')
    
    image = models.ImageField(upload_to='listing/images', default='listing/images/None/NoImage.png')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}. {self.title}, ${self.currentPrice}"

class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bidPrice = models.FloatField(validators=[MinValueValidator(0.1)])
    bidListing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidListing")
    biddedDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Bid by {self.bidder} on {self.bidListing} - Price: {self.bidPrice}"
    

class Comments(models.Model):
    comment = models.CharField(max_length=64)
    

    

    
