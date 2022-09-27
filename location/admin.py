from django.contrib import admin
from .models import City, Address, Province

# Register your models here.
admin.site.register(City)
admin.site.register(Address)
admin.site.register(Province)
