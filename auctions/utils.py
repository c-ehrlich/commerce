import datetime as dt
from datetime import datetime
from .models import Auction, Bid, User


# creates a new auction.
# input: cleaned_data of the create auction form
# output: if successful -> the created auction object | if unsuccessful -> -1
def create_auction(request, data):
    try:
        auction = Auction.objects.create(
            seller = request.user,
            title = data["title"],
            description = data["description"],
            image = data["image"], 
            starting_bid = data["starting_bid"],
            ending_time = datetime.now() + dt.timedelta(days = int(data["duration"]))
        )
        auction.category.set({data["category"]})
        return auction
    except Exception as e:
        print(e)
        return -1


# returns a dictionary with additional information about an auction
def get_auction_status(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    user = User.objects.get(username=request.user.username)

    # is_over
    # indicates whether the auction has ended
    # TODO MAKE SURE I'M NOT DOING INCORRECT TIMEZONE MATH HERE!
    # (using datetime in UTC, make sure the model also uses UTC)
    if auction.ending_time < datetime.now().astimezone(tz=None):
        is_over = True
    else:
        is_over = False

    # is_owner
    # indicates whether or not the user is the owner of the auction
    if user == auction.seller:
        is_owner = True
    else:
        is_owner = False

    # is_watched
    # indicates whether or not the user is currently watching the auction
    if auction in user.watched_auctions.all():
        is_watched = True;
    else:
        is_watched = False;
    
    # create uaction_status variable
    auction_status = {
        "is_over": is_over,
        "is_owner": is_owner,
        "is_watched": is_watched
    }

    return auction_status


# returns an object representing the current bid
def get_current_bid(auction_id):
    auction = Auction.objects.get(pk=auction_id)
    current_bid = {
        "price": auction.starting_bid,
        "bidder": None
    }
    bids = auction.auction_bids.all()
    for bid in bids:
        if bid.value > current_bid["price"]:
            current_bid["price"] = bid.value
            current_bid["bidder"] = bid.user.username
    print(f"current_bid for {auction_id}: {current_bid}")
    return current_bid
    