from django.contrib.auth.models import AbstractUser
from django.db import models

# Remember that each time you change anything in auctions/models.py, 
# you’ll need to first run python manage.py makemigrations and then 
# python manage.py migrate to migrate those changes to your database.
class User(AbstractUser):
    pass
    #id = models.IntegerField()
    #username = models.CharField(max_length=64)
    #name = models.CharField(max_length=100)
    #password should be a hash
    #passwordHash = models.CharField()

class AuctionListings(models.Model):
    #LISTING_CATEGORIES = (
        #('Home'),
        #('Fashion'),
        #('Toys'),
        #('Electronics'),
        #('Baby'),
        #('Automotive'),
        #('Other'),
    #)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    itemTitle = models.CharField(max_length=80)
    itemDescription = models.CharField(max_length=450)
    listingImg = models.CharField(max_length=100)
    initialBid = models.IntegerField()
    #category = models.CharField(max_length=15, choices=LISTING_CATEGORIES)
    isActive = models.BooleanField(default=True)
    date = models.DateField()

#class Bids(models.Model):
    #user = models.CharField(max_length=64)
    #bid = models.IntegerField()

#class Comments(models.Model):
    #user = models.CharField(max_length=64)
    #comment = models.CharField(max_length=280)

    #def __str__(self):
        #return f"{ self.user } commented { self.comment }"