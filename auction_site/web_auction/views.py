from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from .models import Auction, Bid, CustomUser, Transaction
from django.http import HttpResponse
from django.utils import timezone
from .forms import AuctionForm
from .datastructures import DualPriorityQueue, Stack, LinkedList
from django.http import JsonResponse


# Initialize data structures
item_queue = DualPriorityQueue()
bid_stack = Stack()
user_list = LinkedList()
top_bids = []

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Auction, Bid, CustomUser
from .forms import AuctionForm
from .datastructures import DualPriorityQueue, Stack, LinkedList

# Initialize data structures
item_queue = DualPriorityQueue()
bid_stack = Stack()
user_list = LinkedList()

def populate_data_structures():
    item_queue.clear()
    bid_stack.clear()
    user_list.clear()
    # Load current auctions into priority queue
    auctions = Auction.objects.filter(end_time__gt=timezone.now())  # Only current auctions
    for auction in auctions:
        priority = auction.priority  # Primary priority
        secondary_priority = (auction.end_time - timezone.now()).total_seconds()  # Time remaining
        item_queue.push(auction.id, priority, secondary_priority)

    # Load bids into stack
    bids = Bid.objects.all()
    for bid in bids:
        bid_stack.push(bid)
    
    # Load users into linked list
    users = CustomUser.objects.all()
    for user in users:
        user_list.append(user.username)

        

from django.shortcuts import render, get_object_or_404
from .models import Auction, Bid

def index(request):
    populate_data_structures()  # Load data into data structures

    # Get the top auction ID from the priority queue without removing it
    top_auction_id = item_queue.peek()
    top_auction = get_object_or_404(Auction, id=top_auction_id) if top_auction_id else None
    top_bids = []
    top_bid = {}

    # Fetch top bids for the auction
    if top_auction:
        top_bids = top_auction.bids.order_by('-amount')[:3]  # Get top 3 bids
        # Add bidder name to each bid (assuming each bid has a `user` associated with it)
        for bid in top_bids:
            bid.bidder_name = bid.user.username  # Add bidder name to each bid
        top_bid = top_bids[0] if top_bids else None  # Get the highest bid (if exists)
        


    return render(request, 'index.html', {
        'auction': top_auction,
        'top_bids': top_bids,
        'top_bid': top_bid,  # Pass the highest bid
    })




def place_bid(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)

    # Populate user list from the linked list
    users = []
    current_node = user_list.head  # Assuming your LinkedList has a head attribute
    while current_node:
        users.append(current_node.data)  # Replace `data` with the attribute you want to display, e.g., `username`
        current_node = current_node.next  # Move to the next node

    if request.method == 'POST':
        try:
            amount = float(request.POST['amount'])
            selected_user = request.POST.get('user')  # Get the selected user from the form

            if amount < auction.base_amount:
                error_message = "Bid amount is too low."
                return render(request, 'bid_error.html', {'error_message': error_message, 'auction_id': auction.id})

            # Get the last bid for this auction
            last_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()

            if last_bid:
                # Check if the new bid amount is greater than the last bid amount
                if amount <= last_bid.amount:
                    error_message = "Bid amount must be greater than the previous bid amount."
                    return render(request, 'bid_error.html', {'error_message': error_message, 'auction_id': auction.id})

                # Check if the user is different from the last bidder
                if last_bid.user.username == selected_user:
                    error_message = "You cannot place a bid as the same user who made the previous bid."
                    return render(request, 'bid_error.html', {'error_message': error_message, 'auction_id': auction.id})

            # Find the user object based on selected username
            user = CustomUser.objects.get(username=selected_user)

            bid = Bid.objects.create(auction=auction, amount=amount, user=user)
            bid_stack.push(bid)

            return render(request, 'bid_placed.html', {
                'bid_amount': amount,
                'auction_title': auction.title,
                'auction_id': auction.id
            })

        except ValueError:
            error_message = "Invalid bid amount."
            return render(request, 'bid_error.html', {'error_message': error_message, 'auction_id': auction.id})

    return render(request, 'place_bid.html', {'auction': auction, 'users': users})





def view_bids(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    bids = Bid.objects.filter(auction=auction).order_by('-amount')[:3]  # Get top 3 bids
    return render(request, 'view_bids.html', {'auction': auction, 'bids': bids})

def add_auction(request):
    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            auction = form.save()
            priority = int(request.POST.get('priority', 5))
            # Use end_time as the primary priority and the provided priority as the secondary priority
            secondary_priority = (auction.end_time - timezone.now()).total_seconds()
            item_queue.push(auction.id, priority, secondary_priority)
            return redirect('index')  # Redirect to the index page
    else:
        form = AuctionForm()
    return render(request, 'add_auction.html', {'form': form})


def update_auction_priority(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)

    # Reduce the auction's priority
    auction.priority = min(10, auction.priority + 1)
    auction.save()

    # Update the priority in the data structure
    secondary_priority = (auction.end_time - timezone.now()).total_seconds()
    item_queue.update_priority(auction.id, auction.priority, secondary_priority)

    # Peek the next auction
    next_auction_id = item_queue.peek()

    if next_auction_id:
        next_auction = get_object_or_404(Auction, id=next_auction_id)
        return JsonResponse({
            'status': 'success',
            'next_auction': {
                'id': next_auction.id,
                'title': next_auction.title,
                'description': next_auction.description,
                'base_amount': str(next_auction.base_amount),
                'end_time': next_auction.end_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        })

    return JsonResponse({'status': 'no_next_auction'})

def view_auctions(request):
    current_auctions = Auction.objects.filter(end_time__gt=timezone.now())  # Current auctions
    past_auctions = Auction.objects.filter(end_time__lte=timezone.now())  # Past auctions
    return render(request, 'view_auctions.html', {
        'current_auctions': current_auctions,
        'past_auctions': past_auctions
    })
def close_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)

    # Update the end time to the current time
    auction.end_time = timezone.now()
    auction.save()

    # Pop the auction from the priority queue since it is the current auction
    item_queue.pop()  # This will remove the top auction, which is the current one

    return redirect('index')  # Redirect back to the index page




def pay_now(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)

    # Get the top bid
    bidder_name = request.GET.get('bidder_name')
    amount = request.GET.get('amount')

    # Get the top bid for the auction
    top_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()

    if not top_bid:
        return redirect('index')  # If no bids placed, redirect to index

    if not bidder_name or not amount:
        return HttpResponse("No valid bid details provided.", status=400)

    # If it's a POST request, capture transaction details
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')

        if not transaction_id:
            return HttpResponse("Transaction ID is missing.", status=400)

        # Save the transaction
        transaction = Transaction.objects.create(
            auction=auction,
            transaction_id=transaction_id,
            amount_paid=amount,
            bidder_name=bidder_name
        )

        # Mark the auction as closed
        auction.end_time = timezone.now()
        auction.save()

        # Pop the auction from the priority queue since it is now closed
        item_queue.pop()

        # Redirect to payment confirmation page
        return redirect('payment_confirmation', auction_id=auction.id)

    # If not POST, render payment page
    return render(request, 'pay_now.html', {'auction': auction, 'top_bid': top_bid})

def payment_confirmation(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    # Get the latest transaction for the auction
    transaction = Transaction.objects.filter(auction=auction).order_by('-id').first()

    if not transaction:
        return redirect('index')  # If no transaction found, go to the index page

    # Fetch the top bid
    top_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()

    return render(request, 'payment_confirmation.html', {
        'auction': auction,
        'transaction': transaction,
        'top_bid': top_bid
    })

