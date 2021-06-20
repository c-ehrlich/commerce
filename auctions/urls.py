from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("auction/<int:auction_id>", views.auction, name="auction"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist")
]
