from django.contrib import admin
from django.contrib.admin import ModelAdmin

from roomled.models import RoomLEDUser, Device


@admin.register(RoomLEDUser)
class PyNanceUserAdmin(ModelAdmin):
    pass


@admin.register(Device)
class TransactionAdmin(ModelAdmin):
    pass