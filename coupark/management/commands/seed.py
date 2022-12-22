from django.core.management.base import BaseCommand
import logging
logger = logging.getLogger(__name__)

from coupark.models import ParkingSpace, ParkingReservation, Date
from datetime import datetime, timedelta

# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    logger.info("Delete ParkingReservations, ParkingSpaces, and Dates instances")
    ParkingReservation.objects.all().delete()
    ParkingSpace.objects.all().delete()
    Date.objects.all().delete()


spots = [ 
{'name': "Spot: 15", 'description': "Big Spot - S3 (In front of 16)", 'active': True, 'vehicle': "Car"},
{'name': "Spot: 16", 'description': "Big Spot - S3 (Behind 15)", 'active': True, 'vehicle': "Car"},
{'name': "Spot: 43", 'description': "S3 (In front of 44)", 'active': True, 'vehicle': "Car"},
{'name': "Spot: 44", 'description': "S3 (Behind 43)", 'active': True, 'vehicle': "Car"},
{'name': "Spot: 46", 'description': "S3 (In front of 47)", 'active': True, 'vehicle': "Car"},
{'name': "Spot: 47", 'description': "S3 (Behind 46)", 'active': True, 'vehicle': "Car"},
{'name': "Spot: 49", 'description': "S3 (In front of 50)", 'active': True, 'vehicle': "Car"},
{'name': "Spot: 50", 'description': "S3 (Behind 49)", 'active': True, 'vehicle': "Car"},
{'name': "Spot: 52-1", 'description': "S3", 'active': True, 'vehicle': "Motorbike"},
{'name': "Spot: 52-2", 'description': "S3", 'active': True, 'vehicle': "Motorbike"},
{'name': "Spot: 52-3", 'description': "S3", 'active': True, 'vehicle': "Motorbike"},
{'name': "Spot: 52-4", 'description': "S3", 'active': True, 'vehicle': "Motorbike"},
{'name': "Spot: 53-1", 'description': "S3", 'active': True, 'vehicle': "Motorbike"},
{'name': "Spot: 53-2", 'description': "S3", 'active': True, 'vehicle': "Motorbike"},
{'name': "Spot: 53-3", 'description': "S3", 'active': True, 'vehicle': "Motorbike"},
{'name': "Spot: 53-4", 'description': "S3", 'active': True, 'vehicle': "Motorbike"}
]

def add_spots():
    """Adds parking spots"""
    logger.info("Adding Parking Spots")
    
    for spot in spots:
        
        parkingSpot = ParkingSpace(
            name = spot['name'],
            description = spot['description'],
            active = spot['active'],
            vehicleType = spot['vehicle']
        )

        parkingSpot.save()
        logger.info(f"Spot { spot['name'] } created")

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()

    # Adds parkingSpaces
    add_spots()

    #Adds date
    nextDate = datetime.today()
    Date.objects.update_or_create( date = nextDate, defaults={'date':nextDate} )
    dbDate = Date.objects.get(date = nextDate)

    #Adds parking reservations
    parkingLots = ParkingSpace.objects.all()
    for parkingLot in parkingLots:
          if parkingLot.active:
              # Update or create new item to Parking reservation
              ParkingReservation.objects.update_or_create( date = dbDate, parkingSpace = parkingLot, defaults={'user':None, 'date':dbDate, 'parkingSpace':parkingLot})


