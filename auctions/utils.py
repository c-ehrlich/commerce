import datetime as dt
from datetime import datetime
from .models import Auction, Bid, User


# closes an auction, and makes the highest bidder the winner
# if there are no bids, there is no winner
def close_auction_util(request, auction_id):
    auction = get_auction_from_id(auction_id)
    winning_bid = get_current_bid(auction)
    if winning_bid != None:
        auction.winner = winning_bid.user
    auction.is_closed = True
    auction.save()
    return


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
    auction = get_auction_from_id(auction_id)

    # is_over
    # indicates whether the auction has ended
    is_over = has_ended(auction)

    try:
        user = User.objects.get(username=request.user.username)
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

    except Exception as e:
        is_owner = False
        is_watched = False
        print(e, "not logged in")  
        
    # create auction_status variable
    auction_status = {
        "is_over": is_over,
        "is_owner": is_owner,
        "is_watched": is_watched
    }

    return auction_status


# get_auction_from_id(auction_id)
# returns an auction object
# also does additional checks
# currently:
  # is the auction over? if yes, end it
def get_auction_from_id(auction_id):
    auction = Auction.objects.get(pk=auction_id)
    if auction != None:
        if has_ended(auction):
            auction.is_closed = True
            auction.save()
    return auction


# returns an object representing the current bid
def get_current_bid(auction):
    bid = auction.auction_bids.order_by('-value').first()
    if bid != None:
        return bid
    else:
        # TODO maybe return something other than None?
        # some kind of object that gives information about the starting bid?
        return None
    

# checks if an auction has ended
# TODO MAKE SURE I'M NOT DOING INCORRECT TIMEZONE MATH HERE!
# (using datetime in UTC, make sure the model also uses UTC)
def has_ended(auction):
    if auction.ending_time < datetime.now().astimezone(tz=None):
        current_bid = get_current_bid(auction)
        if current_bid != None and auction.winner != None:
            auction.winner.set(current_bid.user)
        auction.save()
        return True
    else:
        return False
