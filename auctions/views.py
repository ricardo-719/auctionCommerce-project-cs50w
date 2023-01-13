from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import AuctionListings
from django import forms
from django.forms import ModelForm, TextInput, Textarea, NumberInput, Select
from .models import User
from datetime import datetime

#class newListing(forms.Form):
    #listingImg = forms.ImageField(label="Image")
class AuctionListingsForm(ModelForm):
    class Meta:
        model = AuctionListings
        exclude = ['user', 'isActive', 'date']
        widgets = {'itemTitle': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px',
                'placeholder': 'Title',
                'label': 'Title'
            }),
            'itemDescription': Textarea(attrs={
               'class': "form-control",
                'cols': 40,
                'rows': 15,
                'style': 'width: 75%',
                'autocomplete': "off",
                'placeholder': 'Description',
                'label': 'Description' 
            }),
            'initialBid': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px',
                'placeholder': 'USD'
            }),
            'category': Select(attrs={
                'class': "form-control",
                'style': 'max-width: 150px'
            }),
            'listingImg': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px',
                'placeholder': 'Image URL',
            })}

def index(request):
    listing = AuctionListings.objects.all()
    return render(request, "auctions/index.html", {
        "listing": listing
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
        return render(request, "auctions/login.html")


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

def new_listings(request):
    #MUST ADD A LOGIN DECORATOR 
    #ADD CURRENT USER INSIDE A VARIABLE AND MUST BE INCLUDED IN THE DATABASE ENTRY
    #listing = AuctionListings.objects.all()
    form = AuctionListingsForm(request.POST)
    # if form.is_valid(): but remember that this field is optional
    if request.method == "POST":
        if form.is_valid():
            title = request.POST["itemTitle"]
            description = request.POST["itemDescription"]
            bid = request.POST["initialBid"]
            category = request.POST["category"]
            imgUrl = request.POST["listingImg"]
            print(title)
            print(description)
            print(bid)
            print(category)
            print(imgUrl)
            print(datetime.now().strftime("%Y/%m/%d, %H:%M"))
            #f = AuctionListings(itemTitle=title, itemDescription=description, initialBid=bid, listingImg=imgUrl, category=category, date=datetime.now().strftime("%Y-%m-%d"))
            #f.save()
        return render(request, "auctions/auctionlisting.html")
    else:
        return render(request, "auctions/auctionlisting.html", {
        "form": AuctionListingsForm()
        })