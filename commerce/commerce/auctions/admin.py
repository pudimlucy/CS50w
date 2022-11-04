from django.contrib import admin
from .models import User, Listing, Watch, Bid, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Watch)
admin.site.register(Bid)
admin.site.register(Comment)
