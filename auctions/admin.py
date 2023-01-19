from django.contrib import admin
from .models import User, AuctionListings, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListings)
admin.site.register(Watchlist)