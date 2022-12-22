from django.core.management.base import BaseCommand
import logging
logger = logging.getLogger(__name__)

from coupark.models import ParkingSpace, ParkingReservation, Date
from datetime import datetime, timedelta

# python manage.py newDay --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

class Command(BaseCommand):
    help = "Create new reservation entries for a new day."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('Creating new reservation entries...')
        run_newDay(self, options['mode'])
        self.stdout.write('done.')

def NewDay():
    """
    Adds a new day
    if tomorrow is not created.
    """

    nextDate = datetime.today() + timedelta(days=1)

    logger.print('Next date: ' + nextDate)
    logger.print('DB Date: ' + Date.objects.last().date)

    if Date.objects.last().date != nextDate:

        parkingLots = ParkingSpace.objects.all()

        newDate = Date(date=nextDate)
        newDate.save()

        for parkingLot in parkingLots:
            if parkingLot.active:
                # Update or create new item to Parking reservation
                ParkingReservation.objects.update_or_create( date = newDate, parkingSpace = parkingLot, defaults={'user':None, 'date':newDate, 'parkingSpace':parkingLot})
        
        logger.info("Next Day created")

    else:
      logger.info("Next Day already created")

def run_newDay(self, mode):
    """ Create a NewDay database

    :param mode: refresh 
    :return:
    """

    if mode == 'refresh':
            
        # Adds a newDay of reservation entries
        newDay()


