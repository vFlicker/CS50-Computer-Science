from datetime import datetime

from django.contrib.auth import get_user_model, models
from django.db import models
from django.db.models import BooleanField, Case, When, Value
from django.db.models.signals import pre_save
from django.dispatch import receiver

from yeticave.categories.models import Category

User = get_user_model()


class ListingQuerySet(models.QuerySet):
    def with_in_watchlist(self, user: User) -> models.QuerySet:
        return self.annotate(
            in_watchlist=Case(
                When(watchlist__owner=user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )


ListingManager = models.Manager.from_queryset(ListingQuerySet)


class Listing(models.Model):
    title: str = models.CharField(max_length=255)
    description: str = models.TextField()
    image_url: str = models.URLField()

    starting_bid: float = models.DecimalField(max_digits=10, decimal_places=2)
    current_price: float = models.DecimalField(max_digits=10, decimal_places=2)

    is_active: bool = models.BooleanField(default=True)

    category: Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creator: User = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = ListingManager()

    def __str__(self):
        return self.title


class Bid(models.Model):
    bid_amount: float = models.DecimalField(max_digits=10, decimal_places=2)

    bid_time: datetime = models.DateTimeField(auto_now_add=True)

    listing: Listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder: User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bid on {self.listing.title} by {self.bidder.username}"


class Comment(models.Model):
    text: str = models.TextField()

    created_at: datetime = models.DateTimeField(auto_now_add=True)

    listing: Listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment on {self.listing.title} by {self.user.username}"


@receiver(pre_save, sender=Listing)
def set_current_price(sender, instance, **kwargs):
    if not instance.current_price:
        instance.current_price = instance.starting_bid
