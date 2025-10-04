from django.contrib import admin
from .models import CustomUser, Client

admin.site.register(CustomUser)
admin.site.register(Client)
