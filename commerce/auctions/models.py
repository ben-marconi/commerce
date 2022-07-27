from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils
import datetime


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", related_name='watchlist', default=None, blank=True)


class Category(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type

class Listing(models.Model):
    title = models.CharField(max_length=100, blank = False)
    description = models.CharField(max_length=1000, blank = True)
    starting = models.PositiveIntegerField()
    image = models.URLField()
    category = models.ForeignKey(Category, related_name = "category", on_delete=models.CASCADE, default = 1, blank = True)
    poster = models.ForeignKey(User, related_name = "postedby", on_delete=models.CASCADE, blank = True, default = 1)
    date = models.DateTimeField(default=django.utils.timezone.now)
    open = models.BooleanField(default=True)
    buyer = models.ForeignKey(User, related_name = "buyer", default = 1, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} posted by {self.poster}"
    

class Bid(models.Model):
    value = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name = "bids",  default = 1)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "bidder")

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name = "comments")
    title = models.CharField(max_length=100, blank = False)
    content = models.CharField(max_length=1000, blank = True)
    commenter = models.ForeignKey(User, related_name = "commenter", on_delete=models.CASCADE, blank = True, default = 1)
    date = models.DateTimeField(default=django.utils.timezone.now)
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return f"{self.title} by {self.commenter}"