from .models import Auction, Bid

def current_bid(auction_id):
	auction = Auction.objects.get(pk=auction_id)
	print(auction)
	price = auction.starting_bid
	bids = auction.auction_bids.all()
	for bid in bids:
		print(f"price: {price}, bid: {bid.value}")
		if bid.value > price:
			price = bid.value
	print(f"current price for {auction_id}: {price}")
	return price

	