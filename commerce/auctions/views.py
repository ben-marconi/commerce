from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
import datetime

DEMO_CHOICES =(
    ("1", "Fashion"),
    ("2", "Electronics"),
    ("3", "Home"),
    ("4", "Toys"),
    ("5", "Other")
)




def index(request):
    listings = Listing.objects.all()
    active = []
    inactive = []
    for listing in listings:
        if listing.open == True:
            active.append(listing)
        else:
            inactive.append(listing)

    return render(request, "auctions/index.html", {"active_listings": active, "inactive_listings": inactive})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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

def new_listing(request):
    if request.method == 'POST':
        poster = request.user
        title = request.POST['title']
        description = request.POST['description']
        starting = request.POST['starting']
        image = request.POST['image']
        category  = Category.objects.get(pk = int(request.POST["category"]))
        listing = Listing(poster = poster, buyer = poster, title = title, description = description, category = category, starting = starting, image = image, open = True)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/newlisting.html", {"categories": Category.objects.all()})


def item(request, item_id):
    listing = Listing.objects.get(id=item_id)
    isowner = (request.user == listing.poster)
    has_bid = listing.poster != listing.buyer
    poster = request.user
    in_watchlist = False
    if request.user.is_authenticated:
        for listin in poster.watchlist.all():
            if listin == listing:
                in_watchlist = True
    if isowner:
        if request.method == 'POST':
            listing.open = False
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        if request.method == 'POST':
            title = request.POST['title']
            content = request.POST['content']
            if (content != "") and (title != ""):    
                comment = Comment(commenter = poster, listing = listing, title = title, content = content)
                comment.save()
                return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/listing.html", {"listing": listing, "comments": listing.comments.all(), "isowner":isowner, "has_bid":has_bid, "in_watchlist": in_watchlist})



def closed(request, item_id):
    poster = request.user
    listing = Listing.objects.get(id=item_id)
    isbuyer = (poster == listing.buyer)
    isowner = (poster == listing.poster)
    in_watchlist = False
    if request.user.is_authenticated:
        for listin in poster.watchlist.all():
            if listin == listing:
                in_watchlist = True
    if request.method == 'POST':
        poster = request.user
        title = request.POST['title']
        content = request.POST['content']
        comment = Comment(commenter = poster, listing = listing, title = title, content = content)
        comment.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/closed.html", {"listing": listing, "comments": listing.comments.all(), "isbuyer":isbuyer, "isowner":isowner, "in_watchlist": in_watchlist})


def bid(request, item_id):
    listing = Listing.objects.get(id=item_id)
    poster = request.user
    isowner = (request.user == listing.poster)
    isbuyer = (request.user == listing.buyer)
    if request.method == 'POST':
        bid = request.POST['bid']
        if str.isnumeric(bid):
            if int(bid) > listing.starting:
                bid = Bid(value=int(bid), listing = listing, bidder = poster)
                bid.save()
                listing.starting = bid.value
                listing.buyer = bid.bidder
                listing.save()
                return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/bid.html", {"listing": listing, "comments": listing.comments.all(), "isbuyer":isbuyer, "isowner":isowner})


def comment(request, item_id):
    listing = Listing.objects.get(id=item_id)
    isowner = (request.user == listing.poster)
    has_bid = listing.poster != listing.buyer
    poster = request.user
    in_watchlist = False
    if request.user.is_authenticated:
        for listin in poster.watchlist.all():
            if listin == listing:
                in_watchlist = True
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        if (content != "") and (title != ""):    
            comment = Comment(commenter = poster, listing = listing, title = title, content = content)
            comment.save()
            return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/comment.html", {"listing": listing, "comments": listing.comments.all(), "isowner":isowner, "has_bid":has_bid, "in_watchlist": in_watchlist})






def watchlist(request, item_id):
    listing = Listing.objects.get(id=item_id)
    isowner = (request.user == listing.poster)
    isbuyer = (request.user == listing.buyer)
    poster = request.user
    in_watchlist = False
    if request.user.is_authenticated:
        for listin in poster.watchlist.all():
            if listin == listing:
                in_watchlist = True
    if request.method == 'POST':
        if in_watchlist:
            poster.watchlist.remove(listing)
        else:
            poster.watchlist.add(listing)
        return HttpResponseRedirect(reverse('my_watchlist'))
    return render(request, 'auctions/watchlist.html', {"in_watchlist": in_watchlist, "listing": listing, "comments": listing.comments.all(), "isbuyer":isbuyer, "isowner":isowner})



def category(request):
    message = "Browse by category"
    return render(request, "auctions/category.html", {"categories": Category.objects.all(), "message": message})


def type(request, category_id):
    cat = Category.objects.get(id=category_id)
    message = f"Category selected: {cat.type}"
    listings = cat.category.all()
    active = []
    inactive = []
    for listing in listings:
        if listing.open == True:
            active.append(listing)
        else:
            inactive.append(listing)
            
        
    return render(request, "auctions/type.html", {"active_listings": active, "inactive_listings": inactive, "categories": Category.objects.all(), "message": message})

def mywatchlist(request):
    poster = request.user
    listings = poster.watchlist.all()
    message = "Items in your watchlist"
    active = []
    inactive = []
    for listing in listings:
        if listing.open == True:
            active.append(listing)
        else:
            inactive.append(listing)
    return render(request, "auctions/my_watchlist.html", {"active_listings": active, "inactive_listings": inactive, "message":message})
