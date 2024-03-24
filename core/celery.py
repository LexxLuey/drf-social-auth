from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
# "sample_app" is name of the root app
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery(
    "core", broker=os.getenv("REDIS_PORT"), backend=os.getenv("REDIS_PORT")
)  # config is the name of the app having setting files

# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
