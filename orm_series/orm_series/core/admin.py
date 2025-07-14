from django.contrib import admin
from core.models import Restaurant, Sale, Rating

# Register your models here.
# to django admin interface

admin.site.register(Restaurant)
admin.site.register(Sale)
admin.site.register(Rating)

