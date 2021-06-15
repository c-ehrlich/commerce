from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime as dt

from django.db.models.deletion import CASCADE

CATEGORIES = (
    ("MO", "Motors"),
    ("FA", "Fashion"),
    ("ME", "Books, Movies & Music"),
    ("EL", "Electronics"),
    ("CO", "Collectibles & Art"),
    ("HO", "Home & Garden"),
    ("SP", "Sporting Goods"),
    ("TO", "Toys & Hobbies"),
    ("BU", "Business & Industrial"),
    ("HE", "Health & Beauty"),
    ("OT", "Other"),
)

class Auction(models.Model):
    seller = models.ForeignKey('User', on_delete=models.CASCADE, related_name="auctions")
    is_closed = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=50000)
    image = models.URLField(default=None)
    placed_time = models.DateTimeField(auto_now_add=True)
    ending_time = models.DateTimeField(default=dt.datetime.now() + dt.timedelta(days=7))
    category = models.CharField(
        max_length = 2,
        choices = CATEGORIES,
        default = "OT"
    )

    def __str__(self):
        return f"{self.id}: {self.title}, placed by {self.seller.username}"

class Bid(models.Model):
    value = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, related_name="auction_bids")
    auction = models.ForeignKey('User', on_delete=models.CASCADE, related_name="user_bids")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.user} bid {self.value} on {self.auction} at {self.timestamp}"

class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=CASCADE, related_name="user_comments")
    auction = models.ForeignKey(Auction, on_delete=CASCADE, related_name="auction_comments") 
    comment = models.TextField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.user} commented '{self.comment}' on {self.auction}"

class User(AbstractUser):
    watched_auctions = models.ManyToManyField(
        Auction,
        blank=True,
        related_name = "watching_users"
    )
    # https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/models/
    # username, CharField 30L
    # first_name, CharField 30L
    # last_name, CharField 30L
    # email, EmailField
    # is_staff, BooleanField
    # date_joined, DateTimeField
    # def get_full_name
    # def get_short_name
    # def email_user