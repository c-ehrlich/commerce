from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("auction/<int:auction_id>", views.auction, name="auction"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
