from django.contrib import admin

from . models import User, Category, Bid, Comment, Listing

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Listing)
