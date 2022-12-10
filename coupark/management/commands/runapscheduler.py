# runapscheduler.py
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

#App imports

from coupark.models import ParkingSpace, ParkingReservation, Date
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def NewDay():
    #Gets list of parking spaces.
    parkingLots = ParkingSpace.objects.all()
    nextDate = datetime.today() + timedelta(days=1)

    Date.objects.update_or_create( date = nextDate, defaults={'date':nextDate} )

    dbDate = Date.objects.get(date = nextDate)

    for parkingLot in parkingLots:
        if parkingLot.active:
            # Update or create new item to Parking reservation
            ParkingReservation.objects.update_or_create( date = dbDate, parkingSpace = parkingLot, defaults={'user':None, 'date':dbDate, 'parkingSpace':parkingLot})


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way. 
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
  """
  This job deletes APScheduler job execution entries older than `max_age` from the database.
  It helps to prevent the database from filling up with old historical records that are no
  longer useful.
  
  :param max_age: The maximum length of time to retain historical job execution records.
                  Defaults to 7 days.
  """
  DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
      NewDay,
      trigger=CronTrigger(day_of_week="mon-sun", hour="18", minute="0"),
      id="NewDay",  # The `id` assigned to each job MUST be unique
      max_instances=1,
      replace_existing=True,
    )
    logger.info("Added job 'NewDay'.")

    scheduler.add_job(
      delete_old_job_executions,
      trigger=CronTrigger(
        day_of_week="sun", hour="00", minute="00"
      ),  # Midnight on Sunday, before start of the next work week.
      id="delete_old_job_executions",
      max_instances=1,
      replace_existing=True,
    )
    logger.info(
      "Added weekly job: 'delete_old_job_executions'."
    )

    try:
      logger.info("Starting scheduler...")
      scheduler.start()
    except KeyboardInterrupt:
      logger.info("Stopping scheduler...")
      scheduler.shutdown()
      logger.info("Scheduler shut down successfully!")