from django.contrib import admin
from .models import Blog,Favorite,Comments,Following,UserProfile,BIO

# Register your models here.
admin.site.register(Blog)
admin.site.register(Favorite)
admin.site.register(Comments)
admin.site.register(Following)
admin.site.register(UserProfile)
admin.site.register(BIO)

