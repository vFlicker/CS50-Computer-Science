from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import LoginForm, RegisteringForm, CreateListingForm
from .models import User, Listing


def index(request):
    return render(request, "auctions/index.html", { "listings": Listing.objects.all() })


def listing(request, id):
    return render(request, "auctions/listing.html")


def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)

        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateListingForm()

    return render(request, "auctions/create_listing.html", {"form": form})


def watchlist(request):
    return render(request, "auctions/watchlist.html")


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
