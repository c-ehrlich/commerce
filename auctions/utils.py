from .models import Auction, Bid

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
	