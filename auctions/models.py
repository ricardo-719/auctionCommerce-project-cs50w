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
    LISTING_CATEGORIES = [
        ('OTH', 'Other'),
        ('HOM', 'Home'),
        ('FAS', 'Fashion'),
        ('TOY', 'Toys'),
        ('ELE', 'Electronics'),
        ('BAB', 'Baby'),
        ('AUT', 'Automotive'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    itemTitle = models.CharField(max_length=80)
    itemDescription = models.CharField(max_length=450)
    # Requires the Pillow library (pip install Pillow)
    listingImg = models.ImageField(max_length=250)
    initialBid = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=15, choices=LISTING_CATEGORIES, default=LISTING_CATEGORIES[0][0])
    isActive = models.BooleanField(default=True)
    date = models.DateField()

    def __str__(self):
        return self.itemTitle

#class Bids(models.Model):
    #user = models.CharField(max_length=64)
    #bid = models.IntegerField()

#class Comments(models.Model):
    #user = models.CharField(max_length=64)
    #comment = models.CharField(max_length=280)

    #def __str__(self):
        #return f"{ self.user } commented { self.comment }"