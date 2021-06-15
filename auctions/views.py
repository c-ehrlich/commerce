from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Auction, Bid, Category, Comment, User


def auction(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    return render(request, "auctions/auction.html", {
        "auction": auction
    })

@login_required
def categories(request):
    return render(request, "auctions/categories.html", {
        # "categories": CATEGORIES
        # TODO ENUMERATE ALL CATEGORIES
    })

@login_required
def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html")
    if request.method == "POST":
        print("POSTING a form")
        # TEMP TODO
        auction = Auction.objects.get(pk=1)
        return render(request, "auctions/auction.html", {
            "auction": auction
        })

def index(request):
    # display a list of all the auctions
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST.get("username")
        password = request.POST.get("password")
        next = request.POST.get("next")
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if next != "None":
                next = next.lstrip("/")
                return HttpResponseRedirect(reverse(next))
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        next = request.GET.get("next")
        return render(request, "auctions/login.html", {
            "next": next
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
