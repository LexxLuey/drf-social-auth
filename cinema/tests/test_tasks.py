from datetime import timedelta
from django.utils import timezone
from celery.contrib.testing.worker import start_worker
from cinema.tasks import task_increase_ranking
from cinema.models import Movie
from core.celery import app
from celery.contrib.testing.tasks import ping
from django.test import TransactionTestCase

class TaskIncreaseRankingTests(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.celery_worker = start_worker(app)
        cls.celery_worker.__enter__()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.celery_worker.__exit__(None, None, None)

    def setUp(self):
        super().setUp()
        # Create a movie with modified_at time 6 minutes ago
        self.movie = Movie.objects.create(
            name="Test Movie",
            status=Movie.Status_Choices.COMING_UP,
            ranking=0,
        )
        self.task = task_increase_ranking.delay() # whatever your method and args are
        self.result = self.task.get()
        
    def test_task_increase_ranking(self):
        self.task.wait()
        # Retrieve the updated movie from the database
        updated_movie = Movie.objects.get(pk=self.movie.pk)

        # Check if the ranking has been increased by 10
        self.assertEqual(updated_movie.ranking, 10)

        # Check if the modified_at time has been updated to current time
        self.assertAlmostEqual(
            updated_movie.modified_at, timezone.now(), delta=timedelta(seconds=2)
        )

        # Check if the task completed successfully
        self.assertEqual(self.task.status, "SUCCESS")
