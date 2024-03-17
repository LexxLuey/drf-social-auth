from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class AccountsEndpointsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def login_response(self):
        # Register a new user
        register_url = reverse("rest_register")
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        register_response = self.client.post(register_url, register_data, format="json")

        # Login with the registered user
        login_url = reverse("rest_login")
        login_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        login_response = self.client.post(login_url, login_data, format="json")
        return login_response

    def test_register_and_login_endpoint(self):
        url = reverse("rest_register")
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse("rest_login")
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_endpoint(self):
        url = reverse("rest_logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_details(self):

        login_response = self.login_response()

        # Extract the access token from the login response
        self.access_token = login_response.data["access"]
        self.refresh_token = login_response.data["refresh"]

        url = "/api/auth/user/"
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("pk", response.data)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)

    def test_verify_token(self):
        login_response = self.login_response()

        # Extract the access token from the login response
        self.access_token = login_response.data["access"]
        self.refresh_token = login_response.data["refresh"]

        url = "/api/auth/token/verify/"
        data = {"token": self.access_token}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        login_response = self.login_response()

        # Extract the access token from the login response
        self.access_token = login_response.data["access"]
        self.refresh_token = login_response.data["refresh"]

        url = "/api/auth/token/refresh/"
        data = {"refresh": self.refresh_token}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("access_expiration", response.data)

    @patch("requests.post")
    def test_google_login(self, mock_post):
        # Mock the response from Google's OAuth 2.0 Playground
        mock_response = {
            "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjA5YmNmODAyOGUwNjUzN2Q0ZDNhZTRkODRmNWM1YmFiY2YyYzBmMGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI2NjQzOTE5NTA2NTgtN2Jsc2hnZTRqZjg2NmVoMm9hNnNoaG1vMWhjMDdzYjguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI2NjQzOTE5NTA2NTgtN2Jsc2hnZTRqZjg2NmVoMm9hNnNoaG1vMWhjMDdzYjguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDA2NjExODUyMDU2MDUwMjE2NTUiLCJlbWFpbCI6ImJpZ2dlc3RsdWV5QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiVGo5aEVWUTd6T0NhSWQ4cmVsTTNUQSIsIm5hbWUiOiJMdWV5IGl5b3JudW1iZSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMdUdwcXJoR0FKRURvdUZaTFhhOHRsNzliZ0tSbkNSTkQwV1RiYUwxVXkxQT1zOTYtYyIsImdpdmVuX25hbWUiOiJMdWV5IiwiZmFtaWx5X25hbWUiOiJpeW9ybnVtYmUiLCJsb2NhbGUiOiJlbiIsImlhdCI6MTcxMDY4NzEwOSwiZXhwIjoxNzEwNjkwNzA5fQ.rDD3lsZPXevUD-8lzxKCKulp_NJ6cgPkOgCcFNMSyxt0s8OoiAQ-NoA4SnuYozB4yMynnWFhwuSuO8v_1V6RULAqDbUj12AtO7FGXZD9bh3AkI_RG3gmjvEOkXU7X9A2AQVx4a5b8Xknaw46b2QzrAKI9ZGTTNHa4vrAcY1b-6SVlwKnWbOeO7lKxM0DzVGJxBsn9QvONdQc4WRbTB-foosx9cZCSWSsFmGMkle7fsVzC0Rgk7Eu64M4bxhOnQYGooJdrd6hb7iAi4vdolE4WkgO1-6_sK-ph5fSn9DTqicKHGXA15t66aQC_QjMqjfWgKqi4zxZt84HPe-H0-xVkA"
        }
        mock_post.return_value.json.return_value = mock_response

        url = reverse("google_login")
        data = {
            "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjA5YmNmODAyOGUwNjUzN2Q0ZDNhZTRkODRmNWM1YmFiY2YyYzBmMGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI2NjQzOTE5NTA2NTgtN2Jsc2hnZTRqZjg2NmVoMm9hNnNoaG1vMWhjMDdzYjguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI2NjQzOTE5NTA2NTgtN2Jsc2hnZTRqZjg2NmVoMm9hNnNoaG1vMWhjMDdzYjguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDA2NjExODUyMDU2MDUwMjE2NTUiLCJlbWFpbCI6ImJpZ2dlc3RsdWV5QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiVGo5aEVWUTd6T0NhSWQ4cmVsTTNUQSIsIm5hbWUiOiJMdWV5IGl5b3JudW1iZSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMdUdwcXJoR0FKRURvdUZaTFhhOHRsNzliZ0tSbkNSTkQwV1RiYUwxVXkxQT1zOTYtYyIsImdpdmVuX25hbWUiOiJMdWV5IiwiZmFtaWx5X25hbWUiOiJpeW9ybnVtYmUiLCJsb2NhbGUiOiJlbiIsImlhdCI6MTcxMDY4NzEwOSwiZXhwIjoxNzEwNjkwNzA5fQ.rDD3lsZPXevUD-8lzxKCKulp_NJ6cgPkOgCcFNMSyxt0s8OoiAQ-NoA4SnuYozB4yMynnWFhwuSuO8v_1V6RULAqDbUj12AtO7FGXZD9bh3AkI_RG3gmjvEOkXU7X9A2AQVx4a5b8Xknaw46b2QzrAKI9ZGTTNHa4vrAcY1b-6SVlwKnWbOeO7lKxM0DzVGJxBsn9QvONdQc4WRbTB-foosx9cZCSWSsFmGMkle7fsVzC0Rgk7Eu64M4bxhOnQYGooJdrd6hb7iAi4vdolE4WkgO1-6_sK-ph5fSn9DTqicKHGXA15t66aQC_QjMqjfWgKqi4zxZt84HPe-H0-xVkA"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)

    @patch("requests.post")
    def test_apple_login_endpoint(self, mock_post):
        mock_response = {
            "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjA5YmNmODAyOGUwNjUzN2Q0ZDNhZTRkODRmNWM1YmFiY2YyYzBmMGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI2NjQzOTE5NTA2NTgtN2Jsc2hnZTRqZjg2NmVoMm9hNnNoaG1vMWhjMDdzYjguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI2NjQzOTE5NTA2NTgtN2Jsc2hnZTRqZjg2NmVoMm9hNnNoaG1vMWhjMDdzYjguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDA2NjExODUyMDU2MDUwMjE2NTUiLCJlbWFpbCI6ImJpZ2dlc3RsdWV5QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiVGo5aEVWUTd6T0NhSWQ4cmVsTTNUQSIsIm5hbWUiOiJMdWV5IGl5b3JudW1iZSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMdUdwcXJoR0FKRURvdUZaTFhhOHRsNzliZ0tSbkNSTkQwV1RiYUwxVXkxQT1zOTYtYyIsImdpdmVuX25hbWUiOiJMdWV5IiwiZmFtaWx5X25hbWUiOiJpeW9ybnVtYmUiLCJsb2NhbGUiOiJlbiIsImlhdCI6MTcxMDY4NzEwOSwiZXhwIjoxNzEwNjkwNzA5fQ.rDD3lsZPXevUD-8lzxKCKulp_NJ6cgPkOgCcFNMSyxt0s8OoiAQ-NoA4SnuYozB4yMynnWFhwuSuO8v_1V6RULAqDbUj12AtO7FGXZD9bh3AkI_RG3gmjvEOkXU7X9A2AQVx4a5b8Xknaw46b2QzrAKI9ZGTTNHa4vrAcY1b-6SVlwKnWbOeO7lKxM0DzVGJxBsn9QvONdQc4WRbTB-foosx9cZCSWSsFmGMkle7fsVzC0Rgk7Eu64M4bxhOnQYGooJdrd6hb7iAi4vdolE4WkgO1-6_sK-ph5fSn9DTqicKHGXA15t66aQC_QjMqjfWgKqi4zxZt84HPe-H0-xVkA",
            "code": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjA5YmNmODAyOGUwNjUzN2Q0ZDNhZTRkODRmNWM1YmFiY2YyYzBmMGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI2NjQzOTE5NTA2NTgtN2Jsc2hnZTRqZjg2NmVoMm9hNnNoaG1vMWhjMDdzYjguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI2NjQzOTE5NTA2NTgtN2Jsc2hnZTRqZjg2NmVoMm9hNnNoaG1vMWhjMDdzYjguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDA2NjExODUyMDU2MDUwMjE2NTUiLCJlbWFpbCI6ImJpZ2dlc3RsdWV5QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiVGo5aEVWUTd6T0NhSWQ4cmVsTTNUQSIsIm5hbWUiOiJMdWV5IGl5b3JudW1iZSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMdUdwcXJoR0FKRURvdUZaTFhhOHRsNzliZ0tSbkNSTkQwV1RiYUwxVXkxQT1zOTYtYyIsImdpdmVuX25hbWUiOiJMdWV5IiwiZmFtaWx5X25hbWUiOiJpeW9ybnVtYmUiLCJsb2NhbGUiOiJlbiIsImlhdCI6MTcxMDY4NzEwOSwiZXhwIjoxNzEwNjkwNzA5fQ.rDD3lsZPXevUD-8lzxKCKulp_NJ6cgPkOgCcFNMSyxt0s8OoiAQ-NoA4SnuYozB4yMynnWFhwuSuO8v_1V6RULAqDbUj12AtO7FGXZD9bh3AkI_RG3gmjvEOkXU7X9A2AQVx4a5b8Xknaw46b2QzrAKI9ZGTTNHa4vrAcY1b-6SVlwKnWbOeO7lKxM0DzVGJxBsn9QvONdQc4WRbTB-foosx9cZCSWSsFmGMkle7fsVzC0Rgk7Eu64M4bxhOnQYGooJdrd6hb7iAi4vdolE4WkgO1-6_sK-ph5fSn9DTqicKHGXA15t66aQC_QjMqjfWgKqi4zxZt84HPe-H0-xVkA"
        }
        mock_post.return_value.json.return_value = mock_response

        url = reverse("apple_login")
        data = {
            "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjA5YmNmODAyOGUwNjUzN2Q0ZDNhZTRkODRmNWM1YmFiY2YyYzBmMGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI2NjQzOTE5NTA2NTgtN2Jsc2hnZTRqZjg2NmVoMm9hNnNoaG1vMWhjMDdzYjguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI2NjQzOTE5NTA2NTgtN2Jsc2hnZTRqZjg2NmVoMm9hNnNoaG1vMWhjMDdzYjguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDA2NjExODUyMDU2MDUwMjE2NTUiLCJlbWFpbCI6ImJpZ2dlc3RsdWV5QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiVGo5aEVWUTd6T0NhSWQ4cmVsTTNUQSIsIm5hbWUiOiJMdWV5IGl5b3JudW1iZSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMdUdwcXJoR0FKRURvdUZaTFhhOHRsNzliZ0tSbkNSTkQwV1RiYUwxVXkxQT1zOTYtYyIsImdpdmVuX25hbWUiOiJMdWV5IiwiZmFtaWx5X25hbWUiOiJpeW9ybnVtYmUiLCJsb2NhbGUiOiJlbiIsImlhdCI6MTcxMDY4NzEwOSwiZXhwIjoxNzEwNjkwNzA5fQ.rDD3lsZPXevUD-8lzxKCKulp_NJ6cgPkOgCcFNMSyxt0s8OoiAQ-NoA4SnuYozB4yMynnWFhwuSuO8v_1V6RULAqDbUj12AtO7FGXZD9bh3AkI_RG3gmjvEOkXU7X9A2AQVx4a5b8Xknaw46b2QzrAKI9ZGTTNHa4vrAcY1b-6SVlwKnWbOeO7lKxM0DzVGJxBsn9QvONdQc4WRbTB-foosx9cZCSWSsFmGMkle7fsVzC0Rgk7Eu64M4bxhOnQYGooJdrd6hb7iAi4vdolE4WkgO1-6_sK-ph5fSn9DTqicKHGXA15t66aQC_QjMqjfWgKqi4zxZt84HPe-H0-xVkA",
            "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjA5YmNmODAyOGUwNjUzN2Q0ZDNhZTRkODRmNWM1YmFiY2YyYzBmMGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI2NjQzOTE5NTA2NTgtN2Jsc2hnZTRqZjg2NmVoMm9hNnNoaG1vMWhjMDdzYjguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI2NjQzOTE5NTA2NTgtN2Jsc2hnZTRqZjg2NmVoMm9hNnNoaG1vMWhjMDdzYjguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDA2NjExODUyMDU2MDUwMjE2NTUiLCJlbWFpbCI6ImJpZ2dlc3RsdWV5QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiVGo5aEVWUTd6T0NhSWQ4cmVsTTNUQSIsIm5hbWUiOiJMdWV5IGl5b3JudW1iZSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMdUdwcXJoR0FKRURvdUZaTFhhOHRsNzliZ0tSbkNSTkQwV1RiYUwxVXkxQT1zOTYtYyIsImdpdmVuX25hbWUiOiJMdWV5IiwiZmFtaWx5X25hbWUiOiJpeW9ybnVtYmUiLCJsb2NhbGUiOiJlbiIsImlhdCI6MTcxMDY4NzEwOSwiZXhwIjoxNzEwNjkwNzA5fQ.rDD3lsZPXevUD-8lzxKCKulp_NJ6cgPkOgCcFNMSyxt0s8OoiAQ-NoA4SnuYozB4yMynnWFhwuSuO8v_1V6RULAqDbUj12AtO7FGXZD9bh3AkI_RG3gmjvEOkXU7X9A2AQVx4a5b8Xknaw46b2QzrAKI9ZGTTNHa4vrAcY1b-6SVlwKnWbOeO7lKxM0DzVGJxBsn9QvONdQc4WRbTB-foosx9cZCSWSsFmGMkle7fsVzC0Rgk7Eu64M4bxhOnQYGooJdrd6hb7iAi4vdolE4WkgO1-6_sK-ph5fSn9DTqicKHGXA15t66aQC_QjMqjfWgKqi4zxZt84HPe-H0-xVkA"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)
