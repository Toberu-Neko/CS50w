from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.validators import URLValidator
from django import forms

from .models import User, Listing

class createListingForm(forms.ModelForm):
    categoryKeys = ["None", "Fasion", "Toys", "Electronics", "Home", "Other"]
    category = forms.ChoiceField(choices=[(x,x) for x in categoryKeys])
    description = forms.CharField(widget=forms.Textarea)
    image = forms.URLField(required=False, validators=[URLValidator()])
    class Meta:
        model = Listing
        fields = ['title', 'description', 'startPrice', 'image', 'category']
    
def index(request):
    listing = Listing.objects.all()
    noItem = False
    if len(listing) == 0:
        noItem = True
    return render(request, "auctions/index.html",{
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

def listing(request, title):
    listing = Listing.objects.get(title=title)
    return render(request, "auctions/listing.html",{
        "listing": listing
    })
@login_required(login_url='/login')
def create_listing(request):
    if request.method == "POST":
        return render(request, "auctions/create.html")
    else:
        return render(request, "auctions/create.html",{
            "form": createListingForm(),
            "categoryKeys": createListingForm().categoryKeys,
        })