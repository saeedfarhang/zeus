from django.contrib import admin

from .models.cafe import Cafe
from .models.cafe_map import CafeCanvas, CafeElement, Point

# Register your models here.
admin.site.register(Cafe)
admin.site.register(CafeElement)
admin.site.register(CafeCanvas)
admin.site.register(Point)
