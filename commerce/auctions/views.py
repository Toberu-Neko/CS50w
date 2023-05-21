from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.validators import URLValidator, MinValueValidator
from django import forms

from .models import User, Listing, Bids, Comments


class bidForm(forms.Form):
    bidPrice = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'placeholder':'Bid'}))
        
class createListingForm(forms.ModelForm):
    categoryKeys = ["None", "Fasion", "Toys", "Electronics", "Home", "Other"]
    category = forms.ChoiceField(choices=[(x,x) for x in categoryKeys])
    
    description = forms.CharField(widget=forms.Textarea)
    image = forms.URLField(required=False, validators=[URLValidator()])
    class Meta:
        model = Listing
        fields = ['title', 'description', 'startPrice', 'image', 'category']
    
def index(request):
    listing = Listing.objects.filter(active=True)
    noItem = False
    if len(listing) == 0:
        noItem = True
    return render(request, "auctions/index.html",{
        "allItems": listing,
        "noItem": noItem
    })
    
#TODO 
def categories(request):
    listing = Listing.objects.all()
    noItem = False
    if len(listing) == 0:
        noItem = True
    return render(request, "auctions/categories.html",{
        "allItems": listing,
        "noItem": noItem
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        users = User.objects.all()
        return render(request, "auctions/login.html", {
        })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def clickListing(request, item_id):
    listing = Listing.objects.get(id=item_id)
    if request.user.is_authenticated:
        if request.user.watchList.filter(id=item_id).exists():
            canAddToWatchlist = False
        else:
            canAddToWatchlist = True
    else:
        canAddToWatchlist = False
    
    if(listing.bids.all().count() == 0):
        listing.currentPrice = listing.startPrice
        currentBidder = "There's no bidder yet."
    else:
        listing.currentPrice = listing.bids.all().order_by('-bidPrice')[0].bidPrice
        currentBidder = listing.bids.all().order_by('-bidPrice')[0].bidder
    listing.save()
    
    
    
    form = bidForm()
    form.fields['bidPrice'].widget.attrs['min'] = listing.currentPrice + 0.01

    return render(request, "auctions/listing.html",{
        "canAddToWatchlist" : canAddToWatchlist,
        "bidForm" : form,
        "listing": listing,
        "currentBidder": currentBidder,
        "Debug" : listing.bids.all().count()
    })
    
@login_required(login_url='/login')
def create_listing(request):
    if request.method == "POST":
        if request.POST["image"] == "":
            t_imgURL = "listing/images/None/NoImage.png"
        else:
            t_imgURL = request.POST["image"]
        
        item = Listing.objects.create(
            title = request.POST["title"],
            description = request.POST["description"],
            startPrice = float(request.POST["startPrice"]),
            currentPrice = float(request.POST["startPrice"]),
            category = request.POST["category"],
            created_by = request.user,
            image = t_imgURL,
        )
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html",{
            "form": createListingForm(),
            "categoryKeys": createListingForm().categoryKeys,
        })
        
@login_required(login_url='/login')
def watchlist(request):
    wlist = request.user.watchList.all()
    noItem = False
    if len(wlist) == 0:
        noItem = True
    return render(request, "auctions/watchlist.html",{
        "watchlist": wlist,
        "noItem": noItem
    })
    
@login_required(login_url='/login')
def addWatchlist(request, item_id):
    listing = Listing.objects.get(id=item_id)
    request.user.watchList.add(listing)
    return HttpResponseRedirect(reverse("Listing", args=(item_id,)))

@login_required(login_url='/login')
def removeWatchlist(request, item_id):
    listing = Listing.objects.get(id=item_id)
    request.user.watchList.remove(listing)
    return HttpResponseRedirect(reverse("Listing", args=(item_id,)))

@login_required(login_url='/login')
def bid(request, item_id):
    if request.method == "POST":        
        listing = Listing.objects.get(id=item_id)
        bidPrice = request.POST["bidPrice"]
        bidPrice = float(bidPrice)
        
        if bidPrice > listing.currentPrice:
            listing.currentPrice = bidPrice
            bid = Bids.objects.create(
                bidder = request.user,
                bidListing = listing,
                bidPrice = bidPrice
            )
            listing.bids.add(bid)
            listing.save()
            bid.save()
        
        return HttpResponseRedirect(reverse("Listing", args=(item_id,)))
    else:
        return HttpResponseRedirect(reverse("Listing", args=(item_id,)))
    
@login_required(login_url='/login')
def closeBid(request, item_id):
    listing = Listing.objects.get(id=item_id)
    if request.user == listing.created_by:
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse("Listing", args=(item_id,)))
    
    else:
        return HttpResponseRedirect(reverse("Listing", args=(item_id,)))

