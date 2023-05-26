from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="CreateListing"),
    path("watchlist", views.watchlist, name="Watchlist"),
    
    path("categories", views.categories, name="Categories"),
    path("categories/<str:category>", views.searchCategory, name="SearchCategory"),
    
    path("listing/<int:item_id>", views.clickListing, name="Listing"),
    path("listing/<int:item_id>/add", views.addWatchlist, name="AddWatchlist"),
    path("listing/<int:item_id>/remove", views.removeWatchlist, name="RemoveWatchlist"),
    path("listing/<int:item_id>/bid", views.bid, name="Bid"),
    path("listing/<int:item_id>/comment", views.comment, name="Comment"),
    path("listing/<int:item_id>/close", views.closeBid, name="CloseBid"),
    
]