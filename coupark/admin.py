from django.contrib import admin
from coupark.models import UserProfileInfo, ParkingSpace, ParkingReservation, Date

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(ParkingSpace)
admin.site.register(ParkingReservation)
admin.site.register(Date)