from django.contrib import admin

# accessing data from database
from .models import Rooms, Topic, Massage

# Register your models here.
admin.site.register(Topic)
admin.site.register(Rooms)
admin.site.register(Massage)
