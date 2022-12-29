from django.contrib.auth.models import AbstractUser
from django.db import models

# Remember that each time you change anything in auctions/models.py, 
# you’ll need to first run python manage.py makemigrations and then 
# python manage.py migrate to migrate those changes to your database.
class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    name = models.CharField(max_length=100)
    user = models.CharField(max_length=64)
    initialBid = models.IntegerField()
    date = models.IntegerField()

class Bids(models.Model):
    user = models.CharField(max_length=64)
    bid = models.IntegerField()

class Comments(models.Model):
    user = models.CharField(max_length=64)
    comment = models.CharField(max_length=280)