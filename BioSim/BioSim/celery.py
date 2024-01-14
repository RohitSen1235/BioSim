import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioSim.settings")

app = Celery("BioSim")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

# Celery Beat Settings
# app.conf.beat_schedule = {
#     'create-daily-log-file': {
#         'task': 'core.logging.create_log_file',
#         'schedule': crontab(hour=16, minute=11),
#         #'args': (2,)
#     }
    
# }

app.autodiscover_tasks()