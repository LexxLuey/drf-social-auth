from datetime import datetime
from django.utils import timezone
from django.db.models import F
from .models import Movie
from core.celery import app


@app.task
def task_increase_ranking():
    print(f"ranking of movies begins and worker is running good")

    # Calculate the time 5 minutes ago
    # five_minutes_ago = timezone.now() - timedelta(minutes=5)

    # Update the rankings of movies that are not currently running
    Movie.objects.exclude(status=Movie.Status_Choices.RUNNING).update(
        ranking=F("ranking") + 10, modified_at=datetime.now()
    )

    return "success"
