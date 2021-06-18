from datetime import datetime
from .models import Auction, Bid, User

# returns a dictionary with additional information about an auction
def get_auction_status(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    user = User.objects.get(username=request.user.username)
    if auction.ending_time < datetime.now().astimezone(tz=None):
        is_over = True
    else:
        is_over = False
    if user == auction.seller:
        is_owner = True
    else:
        is_owner = False
    auction_status = {
        "is_over": is_over,
        "is_owner": is_owner
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
	