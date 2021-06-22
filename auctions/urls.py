from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("auction/<int:auction_id>", views.auction, name="auction"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("close_auction/<int:auction_id>", views.close_auction, name="close_auction"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("place_bid/<int:auction_id>", views.place_bid, name="place_bid"),
    path("register", views.register, name="register"),
    path("toggle_watchlist/<int:auction_id>", views.toggle_watchlist, name="toggle_watchlist"),
    path("watchlist", views.watchlist, name="watchlist")
]
