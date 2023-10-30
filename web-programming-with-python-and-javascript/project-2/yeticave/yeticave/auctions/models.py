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
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    objects = ListingManager()

    def __str__(self):
        return self.title


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid on {self.listing.title} by {self.bidder.username}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.listing.title} by {self.user.username}"


@receiver(pre_save, sender=Listing)
def set_current_price(sender, instance, **kwargs):
    if not instance.current_price:
        instance.current_price = instance.starting_bid
