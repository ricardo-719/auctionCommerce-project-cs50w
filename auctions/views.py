from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import AuctionListings, User, Watchlist, Bids
from django import forms
from django.forms import ModelForm, TextInput, Textarea, NumberInput, Select
from datetime import datetime
from django.contrib import messages

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
                'style': 'max-width: 150px',
                'id': 'categoryFormId'
            }),
            'listingImg': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px',
                'placeholder': 'Image URL',
            })}

def index(request):
    listing = AuctionListings.objects.all()
    if request.method == "POST":
        queryCategory = request.POST["category"]
        filteredListing = AuctionListings.objects.filter(category=queryCategory)
        return render(request, "auctions/index.html", {
            "listing": filteredListing,
            "form": AuctionListingsForm()
        })
    else:
        return render(request, "auctions/index.html", {
            "listing": listing,
            "form": AuctionListingsForm()
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
    #listing = AuctionListings.objects.all()
    form = AuctionListingsForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            title = request.POST["itemTitle"]
            description = request.POST["itemDescription"]
            bid = request.POST["initialBid"]
            category = request.POST["category"]
            imgUrl = request.POST["listingImg"]
            print(request.user)
            print(title)
            print(description)
            print(bid)
            print(category)
            print(imgUrl)
            print(datetime.now().strftime("%Y/%m/%d, %H:%M"))
            f = AuctionListings(user=request.user, itemTitle=title, itemDescription=description, initialBid=bid, listingImg=imgUrl, category=category, date=datetime.now().strftime("%Y-%m-%d"))
            f.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/auctionlisting.html", {
        "form": AuctionListingsForm()
        })

def listings_page(request, name):
    item = AuctionListings.objects.filter(itemTitle=name)
    watchlistStatus = Watchlist.objects.filter(itemTitle=name)
    currentBid = 0
    if request.method == "POST":
        # If user is not logged in redirect to login page
        if request.user.is_authenticated:
            activePrice=0
            if Bids.objects.filter(itemTitle=name):
                # Django query that filters and orders by bid amount taking highest bid
                highestBid = Bids.objects.filter(itemTitle=name).order_by('bid')
                for bid in highestBid:
                    currentBid = bid.bid
                    activePrice = bid.bid
            else:
                for bid in item:
                    activePrice = bid.initialBid
            bidRequest = request.POST["bidForm"]
            if float(bidRequest) > activePrice:
                for el in item:
                    itemName = el.itemTitle
                f = Bids(user=request.user, itemTitle=itemName, bid=bidRequest)
                f.save()
                currentBid = float(bidRequest)
                print(currentBid)
                #flash success message (maybe)
                messages.add_message(request, messages.SUCCESS, 'Your bid has been submitted!')
                print('success!')
                return render(request, "auctions/listingPage.html", {
                    "item": item,
                    "watchlistStatus": watchlistStatus,
                    "currentBid": currentBid
                })
            else:
                #flash error message user
                messages.add_message(request, messages.INFO, 'Your bid must be the hightest, please try again.')
                print('Submission failed')
                return render(request, "auctions/listingPage.html", {
                    "item": item,
                    "watchlistStatus": watchlistStatus,
                    "currentBid": currentBid
                })
        else:
            return render(request, "auctions/login.html")  
    else:
        if Bids.objects.filter(itemTitle=name):
            # Django query that filters and orders by bid amount taking highest bid
            highestBid = Bids.objects.filter(itemTitle=name).order_by('bid')
            for bid in highestBid:
                currentBid = bid.bid
                winnerUser = bid.user
            return render(request, "auctions/listingPage.html", {
                "item": item,
                "watchlistStatus": watchlistStatus,
                "currentBid": currentBid,
                "winnerUser": winnerUser
            })
        else:
            winnerUser = 'no one'
            return render(request, "auctions/listingPage.html", {
                "item": item,
                "watchlistStatus": watchlistStatus,
                "currentBid": currentBid,
                "winnerUser": winnerUser
            })

# This function handles the watchlist requests
def watchlist_registry(request):
    if request.method == "POST":
        # If user is not logged in redirect to login page
        if request.user.is_authenticated:
            item = request.POST["title"]
            if Watchlist.objects.filter(itemTitle=item):
                itemDb = Watchlist.objects.get(itemTitle=item)
                itemDb.delete()
                return HttpResponseRedirect(item)
            else:
                f = Watchlist(user=request.user, itemTitle=item)
                f.save()
                return HttpResponseRedirect(item)
        else:
            return render(request, "auctions/login.html")
    else:
        return HttpResponseRedirect(reverse("index"))

#This function handle end auctions requests
def close_listing(request):
    if request.method == "POST":
        # Verify user is log in and is owner of listing
        user = request.user
        owner = request.POST["listingOwner"]
        if request.user.is_authenticated and str(user) == owner:
            item = request.POST["closeListing"]
            try:
                itemDb = AuctionListings.objects.get(itemTitle=item)
                itemDb.isActive = False
                itemDb.save()
                messages.success(request, "Auction has been successfully closed.")
            except:
                messages.info(request, "Something went wrong...")
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html")
    else:
        return HttpResponseRedirect(reverse("index"))

# This function filters all closed listings
def inactive_listing(request):
    listing = AuctionListings.objects.all()
    # For the post method consider adding filter option by listing bidded and owned
    if request.method == "POST":
        queryCategory = request.POST["category"]
        filteredListing = AuctionListings.objects.filter(category=queryCategory)
        return render(request, "auctions/closedListing.html", {
            "listing": filteredListing,
            "form": AuctionListingsForm()
        })
    else:
        return render(request, "auctions/closedListing.html", {
            "listing": listing,
            "form": AuctionListingsForm()
        })