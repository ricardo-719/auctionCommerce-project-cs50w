from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listings, name="newListing"),
    path("watchlist", views.watchlist_registry, name="watchlist"),
    path("close", views.close_listing, name="close"),
    path("inactive", views.inactive_listing, name="inactive"),
    path("comment", views.add_comment, name="comment"),
    path("delComment", views.delete_comment, name="delComment"),
    path("<str:name>", views.listings_page, name="listings")
]
