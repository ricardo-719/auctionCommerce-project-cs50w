from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    LISTING_CATEGORIES = [
        ('STD', 'Standard'),
        ('CLS', 'Classic'),
        ('MDN', 'Modern'),
        ('ELE', 'Electronic'),
        ('TVL', 'Travel'),
        ('LUX', 'Luxury'),
        ('ATQ', 'Antique'),
        ('OTH', 'Other')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    itemTitle = models.CharField(max_length=80)
    itemDescription = models.CharField(max_length=450)
    # ImageField requires the Pillow library (pip install Pillow), this field is optional
    listingImg = models.CharField(max_length=250, null=True, blank=True)
    initialBid = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=15, choices=LISTING_CATEGORIES, default=LISTING_CATEGORIES[0][0])
    isActive = models.BooleanField(default=True)
    date = models.DateField()

    def __str__(self):
        return self.itemTitle

# Consider changing itemTitle to ForeignKey for better manipulation of the databases
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    itemTitle = models.CharField(max_length=80)

    def __str__(self):
        return self.itemTitle

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    itemTitle = models.CharField(max_length=80)
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{ self.itemTitle } / Bid: { self.bid } / User: { self.user }"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    itemTitle = models.CharField(max_length=80)
    comment = models.CharField(max_length=280)
    date = models.DateField()

    def __str__(self):
        return f"{ self.user } commented { self.comment } in { self.itemTitle }"