from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
class User(AbstractUser):
    watchList = models.ManyToManyField('Listing', blank=True, related_name="watchList")
    
    
class Listing(models.Model):
    categoryKeys = ["None", "Fasion", "Toys", "Electronics", "Home", "Other"]
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=64, choices=[(x,x) for x in categoryKeys])
    description = models.CharField(max_length=2048)
    
    startPrice = models.FloatField(validators=[MinValueValidator(0.1)])
    currentPrice = models.FloatField(validators=[MinValueValidator(0.1)], default=startPrice)
    
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder", null=True, blank=True)
    bids = models.ManyToManyField('Bids', blank=True, related_name='listing_bids')
    comments = models.ManyToManyField('Comments', blank=True, related_name='listing_comments')
    
    image = models.URLField(blank=True, null=True)
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
    commentTime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    com_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="com_listing")
    def __str__(self):
        return f"{self.user} commented on {self.com_listing} at {self.commentTime}"
    
    
    

    

    
