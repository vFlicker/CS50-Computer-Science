from django.contrib import admin

from . models import Category, Bid, Comment, Listing, Watchlist

admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(Watchlist)
