# from datetime import datetime
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Auction, Bid, Category, Comment, User
import auctions.utils as utils
import datetime
from decimal import Decimal


# TODO break forms out into their own file
class NewAuctionForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(
        label="Auction Text",
        widget=forms.Textarea
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        to_field_name="category"
    )
    image = forms.URLField(
        label="Image URL",
        initial='http://'
    )
    starting_bid = forms.DecimalField(
        label="Starting Bid",
        decimal_places=2,
        min_value=1,
        max_value=100000
        # default=1
    )
    duration = forms.ChoiceField(
        label="Auction Duration",
        choices = (
            ("1", "1 Day"),
            ("3", "3 Days"),
            ("5", "5 Days"),
            ("7", "7 Days"),
            ("10", "10 Days")
        )
    )



class NewBidForm(forms.Form):
    bid = forms.DecimalField(
        label="Bid",
        decimal_places=2,
        # min_value=1,
        max_value=100000
    )


class NewCommentForm(forms.Form):
    comment = forms.CharField(
        label = "Comment",
        max_length=2000
    )


# adds a comment to an auction
def add_comment(request):
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            next = request.POST.get('next', '/')
            comment = Comment.objects.create(
                comment = data["comment"],
                timestamp = datetime.datetime.now(),
                user = request.user,
                auction = utils.get_auction_from_id(request.POST.get("auction_id"))
            )
        return HttpResponseRedirect(next)


# view an auction
# returns auction (auction object)
def auction(request, auction_id):
    auction = utils.get_auction_from_id(auction_id)
    current_bid = utils.get_current_bid(auction)
    
    # set auction_status ..
    auction_status = utils.get_auction_status(request, auction_id)

    return render(request, "auctions/auction.html", {
        "auction": auction,
        "current_bid": current_bid,
        "auction_status": auction_status,
        "comment_form": NewCommentForm(),
        "place_bid_form": NewBidForm()
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def category(request, category_id):
    # category_id = request.GET.get("category.id")
    category = Category.objects.get(pk=category_id)
    return render(request, "auctions/category.html", {
        "category": category,
        "auctions": category.auctions_with_category.all()
    })


@login_required
def close_auction(request, auction_id):
    if request.method == "POST":
        utils.close_auction_util(request, auction_id)
        return HttpResponseRedirect(reverse("auction", args=(auction_id,)))


@login_required
def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html",{
            "form": NewAuctionForm()
        })
    if request.method == "POST":
        # TODO make sure the auction start and end dates are in UTC
        # (and then we convert to local timezone at runtime)
        form = NewAuctionForm(request.POST)
        if form.is_valid():
            auction = utils.create_auction(request, form.cleaned_data)
        else:
            print("form not valid")
            print(form.errors)
        return HttpResponseRedirect(reverse("auction", args=(auction.id,)))


def index(request):
    # display a list of all the auctions
    auctions = Auction.objects.all() # TODO filter out auctions that have been closed
    
    # exclude auctions that have ended
    excludes = []
    for auction in auctions.all():
        if utils.has_ended(auction):
            excludes.append(auction.id)
    auctions = auctions.exclude(id__in=excludes)

    # add winning bid
    # TODO

    return render(request, "auctions/index.html", {
        "auctions": auctions
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
    

def place_bid(request, auction_id):
    bid = Decimal(request.POST.get('bid'))
    auction = utils.get_auction_from_id(auction_id)
    current_bid = utils.get_current_bid(auction)
    increment = Decimal(0.01)
    if current_bid != None:
        minimum_bid = current_bid.value + increment
    else:
        minimum_bid = auction.starting_bid + increment
    print(f"bid: {bid}, minimum bid: {minimum_bid}")
    if bid < minimum_bid:
        # TODO inject error message somehow
        pass
    else:
        new_bid = Bid.objects.create(
            value = bid,
            user = request.user,
            auction = auction
        )
    return HttpResponseRedirect(reverse("auction", args=(auction.id,))) 


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


@login_required
def toggle_watchlist(request, auction_id):
    next = request.POST.get('next', '/')
    auction = utils.get_auction_from_id(auction_id)
    user = User.objects.get(username=request.user.username)
    
    if auction in user.watched_auctions.all():
        user.watched_auctions.remove(auction)
    else:
        user.watched_auctions.add(auction)

    return HttpResponseRedirect(next)


@login_required
def watchlist(request):
    if request.method == "GET":
        watchlist = request.user.watched_auctions.order_by("ending_time").all()
        
        ended_list = []
        for item in watchlist:
            item.highest_bid = utils.get_current_bid(item)
            if utils.has_ended(item):
                ended_list.append(item.id)
        watchlist_ended = watchlist.filter(id__in=ended_list)
        watchlist = watchlist.exclude(id__in=ended_list)

        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist,
            "watchlist_ended": watchlist_ended
        })