from apscheduler.schedulers.blocking import BlockingScheduler

from email_service.reminder_job import process_reminders

scheduler = BlockingScheduler()

scheduler.add_job(
    process_reminders,
    'interval',
    hours=24
)

scheduler.start()
