from rest_framework.test import APITestCase

from users.models import User
from teams.models import Team
from players.models import Player
from championships.models import Championship


class UserViewerTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "name": "Xuxa Meneguel",
            "email": "xuxa@mail.com",
            "password": "ilarilarie",
            "birthdate": "1964-10-10",
        }
        cls.superuser_data = {
            "name": "Adamastor",
            "email": "adamastor@mail.com",
            "password": "123456",
            "birthdate": "1999-09-09",
            "genre": "Masculino",
        }
        cls.superuser = User.objects.create_superuser(**cls.superuser_data)

        cls.expected_keys = {
            "id",
            "name",
            "email",
            "birthdate",
            "is_superuser",
            "is_active",
            "genre",
            "created_at",
            "updated_at",
            "favorite_teams",
            "favorite_players",
            "favorite_championships",
        }

    def test_can_register_new_user(self):
        response = self.client.post("/api/register/", self.user_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.expected_keys, set(response.data.keys()))

    def test_cannot_register_new_user(self):
        response = self.client.post("/api/register/", {})

        self.assertEqual(response.status_code, 400)

    def test_login(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        response = self.client.post("/api/login/", login_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual({"token"}, set(response.data.keys()))

    def test_list_users(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.get("/api/users/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, response.data["count"])

    def test_retrieve_user(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        user = User.objects.create_user(**self.user_data)

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.get(f"/api/users/{user.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.expected_keys, set(response.data.keys()))

    def test_update_user(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        user = User.objects.create_user(**self.user_data)

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.patch(f"/api/users/{user.id}/", {"name": "jorge"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.expected_keys, set(response.data.keys()))
        self.assertEqual("jorge", response.data["name"])

    def test_disable_user(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        user = User.objects.create_user(**self.user_data)

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.patch(
            f"/api/users/{user.id}/enable_disable/", {"is_active": False}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.expected_keys, set(response.data.keys()))
        self.assertFalse(response.data["is_active"])
