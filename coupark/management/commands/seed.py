from django.core.management.base import BaseCommand
import logging
logger = logging.getLogger(__name__)

from coupark.models import ParkingSpace, ParkingReservation, Date

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
    logger.info("Delete Address instances")
    ParkingReservation.objects.all().delete()
    ParkingSpace.objects.all().delete()
    Date.objects.all().delete()


def add_spots():
    """Adds parking spots"""
    logger.info("Adding Parking Spots")
    street_flats = ["#221 B", "#101 A", "#550I", "#420G", "#A13"]
    street_localities = ["Bakers Street", "Rajori Gardens", "Park Street", "MG Road", "Indiranagar"]
    pincodes = ["101234", "101232", "101231", "101236", "101239"]

    address = Address(
        street_flat=random.choice(street_flats),
        street_locality=random.choice(street_localities),
        pincode=random.choice(pincodes),
    )
    address.save()
    logger.info("{} address created.".format(address))
    return address

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()

    # Creating 15 addresses
    for i in range(15):
        create_address()