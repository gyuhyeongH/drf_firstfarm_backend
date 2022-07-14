from django.contrib import admin
from .models import User, UserProfile, UserCategory, Rank

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(UserCategory)
admin.site.register(Rank)