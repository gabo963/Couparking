from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
# Create your models here.

class UserProfileInfo( models.Model ):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #  Additional classes
    profile_pic = models.ImageField( upload_to='profile_pics', blank = True )

    def __str__(self):
        return self.user.username

def validate_ParkingSpace_vehicle_type(value):
    if not (value == 'Car' or value == 'Motorbike'):
        raise value.ValidationError("Vehicle Type not allowed")

class ParkingSpace( models.Model ):
    
    name = models.CharField( max_length=15 )
    description = models.CharField( max_length=100 )
    active = models.BooleanField( default = True )
    vehicleType = models.CharField(max_length=15, validators=[validate_ParkingSpace_vehicle_type])

    def __str__(self):
        return str(self.name)

class Date( models.Model ):
    date = models.DateField()

    def __str__(self):
        return str(self.date)

class ParkingReservation( models.Model ):

    parkingSpace = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE)
    user = models.ForeignKey( User, on_delete=models.CASCADE, blank=True, null=True )
    date = models.ForeignKey( Date, on_delete=models.CASCADE )

    def __str__(self):
        return  self.parkingSpace.name + ' ' + str(self.date.date)


