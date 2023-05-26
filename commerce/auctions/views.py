from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.validators import URLValidator, MinValueValidator
from django import forms

from .models import User, Listing, Bids, Comments

class commentForm(forms.Form):
    comment = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder':'Comment'}))
    
class bidForm(forms.Form):
    bidPrice = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'placeholder':'Bid'}))
        
class createListingForm(forms.ModelForm):
    categoryKeys = ["None", "Fasion", "Toys", "Electronics", "Home", "Other"]
    category = forms.ChoiceField(choices=[(x,x) for x in categoryKeys])
    
    description = forms.CharField(widget=forms.Textarea)
    image = forms.URLField(required=False, validators=[URLValidator()])
    startPrice = forms.FloatField(validators=[MinValueValidator(0.1)])
    class Meta:
        model = Listing
        fields = ['title', 'description', 'startPrice', 'image', 'category']
    
def index(request):
    listing = Listing.objects.filter(active=True)
    noItem = False
    for item in listing:
        if item.bids.all().count() > 0:
            item.currentPrice = item.bids.all().order_by('-bidPrice')[0].bidPrice
            item.save()
        
    if len(listing) == 0:
        noItem = True
    return render(request, "auctions/index.html",{
        "allItems": listing,
        "noItem": noItem
    })
    
def categories(request):
    categoryKeys = ["None", "Fasion", "Toys", "Electronics", "Home", "Other"]
    
    return render(request, "auctions/categories.html",{
        "categoryKeys": categoryKeys
    })
def searchCategory(request, category):
    listing = Listing.objects.filter(category=category, active=True)

    for item in listing:
        if item.bids.all().count() > 0:
            item.currentPrice = item.bids.all().order_by('-bidPrice')[0].bidPrice
            item.save()
            
    if len(listing) == 0:
        noItem = True
    else:
        noItem = False
        
    return render(request, "auctions/searchCategory.html",{
        "category" : category,
        "allItems" : listing,
        "noItem" : noItem
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
    
    if listing.comments.all().count() == 0:
        noComment = True
    else:
        noComment = False
    
    b_form = bidForm()
    b_form.fields['bidPrice'].widget.attrs['min'] = listing.currentPrice + 0.01

    c_form = commentForm()
    c_form.fields['comment'].widget.attrs['placeholder'] = "Comment"
    c_form.fields['comment'].widget.attrs['rows'] = 3
    return render(request, "auctions/listing.html",{
        "canAddToWatchlist" : canAddToWatchlist,
        "bidForm" : b_form,
        "listing": listing,
        "currentBidder": currentBidder,
        
        "commentForm" : c_form,
        "noComment" : noComment,
        "comments" : listing.comments.all(),
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
        form = createListingForm()
        form.fields['startPrice'].widget.attrs['min'] = 0.1
        return render(request, "auctions/create.html",{
            "form": form,
            "categoryKeys": createListingForm().categoryKeys,
        })
        
@login_required(login_url='/login')
def watchlist(request):
    listing = request.user.watchList.all()
    
    for item in listing:
        if item.bids.all().count() > 0:
            item.currentPrice = item.bids.all().order_by('-bidPrice')[0].bidPrice
            item.save()
            
    noItem = False
    if len(listing) == 0:
        noItem = True
    
    return render(request, "auctions/watchlist.html",{
        "watchlist": listing,
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
    
@login_required(login_url='/login')
def comment(request, item_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=item_id)
        commentStr = request.POST["comment"]
        
        commentObj = Comments.objects.create(
            comment = commentStr,
            user = request.user,
            com_listing = listing
        )
        listing.comments.add(commentObj)
        listing.save()
        commentObj.save()
        return HttpResponseRedirect(reverse("Listing", args=(item_id,)))
    else:
        return HttpResponseRedirect(reverse("Listing", args=(item_id,)))
    
