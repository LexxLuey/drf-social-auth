from django.test import TestCase, Client
from cinema.api import router
from cinema.models import Movie
from ninja.testing import TestClient


class MovieEndpointTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.ninja_client = TestClient(router)

    def test_create_movie(self):
        payload = {
            "name": "Test Movie",
            "protagonists": "Test Protagonist",
            "start_date": "2024-03-25T12:00:00Z",
            "status": 1,
            "ranking": 0,
        }
        response = self.ninja_client.post("/", payload)
        self.assertEqual(response.status_code, 201)

    def test_get_movie(self):
        movie = Movie.objects.create(
            name="Test Movie",
            protagonists="Test Protagonist",
            start_date="2024-03-25T12:00:00Z",
            status=1,
            ranking=0,
        )
        response = self.client.get(f"/api/cinema/{movie.id}")
        self.assertEqual(response.status_code, 200)

    def test_list_movies(self):
        response = self.client.get("/api/cinema/")
        self.assertEqual(response.status_code, 200)

    def test_update_movie(self):
        movie = Movie.objects.create(
            name="Test Movie",
            protagonists="Test Protagonist",
            start_date="2024-03-25T12:00:00Z",
            status=1,
            ranking=0,
        )

        payload = {
            "name": "Updated Test Movie",
            "protagonists": "Updated Test Protagonist",
            "start_date": "2024-03-25T12:00:00Z",
            "status": 1,
            "ranking": 0,
        }
        response = self.ninja_client.put(f"/{movie.id}", payload)
        self.assertEqual(response.status_code, 200)

    def test_delete_movie(self):
        movie = Movie.objects.create(
            name="Test Movie",
            protagonists="Test Protagonist",
            start_date="2024-03-25T12:00:00Z",
            status=1,
            ranking=0,
        )
        response = self.client.delete(f"/api/cinema/{movie.id}")
        self.assertEqual(response.status_code, 204)
