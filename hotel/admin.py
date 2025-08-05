from django.contrib import admin

from hotel.models import Hotel, Guest, Stay


admin.site.register(Hotel)
admin.site.register(Guest)
admin.site.register(Stay)