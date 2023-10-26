from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.views import View


from .forms import LoginForm, RegisteringForm, ListingForm, BidForm
from .models import User, Bid, Listing, Watchlist


class ListingView(View):
    # TODO: Якщо користувач увійшов до облікового запису і він є автором аукціону, він повинен мати змогу «закрити» аукціон на цій сторінці, що зробить автора найбільшої ставки переможцем аукціону, а сам аукціон стане неактивним.

    # TODO: Якщо користувач увійшов до облікового запису на сторінці закритого аукціону і він є переможцем цього аукціону, він має отримати повідомлення про це.

    # TODO: Користувачі, які увійшли до облікових записів, повинні мати можливість додавати коментарі на сторінці аукціону. Сторінка аукціону має відображати всі коментарі, які було зроблено щодо цього аукціону.

    template_name = "auctions/listing.html"
    form_bid = BidForm

    def get(self, request, listing_id):
        listing = Listing.objects.get(pk=listing_id)
        bids = Bid.objects.filter(listing=listing).order_by("-bid_time")[:10]
        is_creator = request.user.is_authenticated and listing.creator == request.user

        context = {
            "listing": listing,
            "form_bid": self.form_bid(),
            "is_creator": is_creator,
            "bids": bids
        }

        return render(request, "auctions/listing.html", context)

    def post(self, request, listing_id):
        listing = Listing.objects.get(pk=listing_id)
        bids = Bid.objects.filter(listing=listing).order_by("-bid_time")[:10]
        is_creator = request.user.is_authenticated and listing.creator == request.user
        form_type = request.POST.get("form_type")

        if form_type == "bid" and not is_creator:
            form_bid = self.form_bid(request.POST)
            if form_bid.is_valid():
                bid = form_bid.save(commit=False)
                bid.listing = listing
                bid.bidder = request.user
                if bid.bid_amount > listing.current_price:
                    bid.save()
                    listing.current_price = bid.bid_amount
                    listing.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    form_bid.add_error(
                        'bid_amount', 'Bid must be greater than the current price.')
        else:
            form_bid = self.form_bid()

        context = {
            "listing": listing,
            "form_bid": form_bid,
            "is_creator": is_creator,
            "bids": bids
        }

        return render(request, "auctions/listing.html", context)


@login_required
def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    if request.method == "POST":
        form = BidForm(request.POST)

        if form.is_valid():
            bid = form.save(commit=False)
            bid.listing = listing
            bid.user = request.user
            if bid.bid_amount > listing.current_price:
                bid.save()
                listing.current_price = bid.bid_amount
                listing.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                form.add_error(
                    'bid_amount', 'Bid must be greater than the current price.')
    else:
        form = BidForm()

    return render(request, "auctions/listing.html", {"listing": listing, "form": form})


def index(request):
    # TODO: Має дозволити користувачам переглянути всі АКТИВНІ АУКЦІОНИ.

    # Check if the user is authenticated (logged in)
    if request.user.is_authenticated:
        # If the user is logged in, get a list of all products and add the in_watchlist flag for each product
        listings = Listing.objects.all().prefetch_related(
            Prefetch(
                'watchlist_set',
                queryset=Watchlist.objects.filter(user=request.user),
                to_attr='in_watchlist'
            )
        )
    else:
        # If the user is not logged in, simply get a list of all products without the in_watchlist flag
        listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def listing(request, listing_id):
    # TODO: Якщо користувач увійшов до облікового запису і він є автором аукціону, він повинен мати змогу «закрити» аукціон на цій сторінці, що зробить автора найбільшої ставки переможцем аукціону, а сам аукціон стане неактивним.

    # TODO: Якщо користувач увійшов до облікового запису на сторінці закритого аукціону і він є переможцем цього аукціону, він має отримати повідомлення про це.

    # TODO: Користувачі, які увійшли до облікових записів, повинні мати можливість додавати коментарі на сторінці аукціону. Сторінка аукціону має відображати всі коментарі, які було зроблено щодо цього аукціону.
    return render(request, "auctions/listing.html", {"listing": Listing.objects.get(pk=listing_id)})


def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()

    return render(request, "auctions/create_listing.html", {"form": form})


@login_required
def watchlist(request):
    # Get a list of all products that are in the tracking list for the current user
    listings = Listing.objects.filter(
        watchlist__user=request.user
    ).prefetch_related(
        Prefetch(
            'watchlist_set',
            queryset=Watchlist.objects.filter(user=request.user),
            to_attr='in_watchlist'
        )
    )

    return render(request, "auctions/watchlist.html", {
        "listings": listings,
    })


@login_required
def toggle_watchlist(request, listing_id):
    item = get_object_or_404(Listing, pk=listing_id)
    watchlist_item, created = Watchlist.objects.get_or_create(
        user=request.user, item=item)

    if not created:
        watchlist_item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Attempt to sign user in
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "auctions/login.html", {
                    "form": form,
                    "message": "Invalid username and/or password."
                })
    else:
        form = LoginForm()

    return render(request, "auctions/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        form = RegisteringForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            confirmation = form.cleaned_data["confirmation"]

            # Ensure password matches confirmation
            if password != confirmation:
                return render(request, "auctions/register.html", {
                    "form": form,
                    "message": "Passwords must match."
                })

            # Attempt to create new user
            user = User.objects.create_user(username, email, password)
            user.save()

            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        form = RegisteringForm()

    return render(request, "auctions/register.html", {"form": form})
