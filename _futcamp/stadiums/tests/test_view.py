from rest_framework.test import APITestCase
from stadiums.models import Stadium
from users.models import User


class StadiumViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.stadium_data = {
            "name": "Piracanjuba",
            "description": "Lugar onde o filho chora e a mãe não vê",
            "capacity": 1000,
            "localizations": "Recife",
            "area": 1000,
        }

        cls.stadium = Stadium.objects.create(**cls.stadium_data)

        cls.superuser_data = {
            "name": "Adamastor",
            "email": "adamastor@mail.com",
            "password": "123456",
            "birthdate": "1999-09-09",
            "genre": "Masculino",
        }
        cls.superuser = User.objects.create_superuser(**cls.superuser_data)

    def test_create_stadium(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        stadium_response = self.client.post("/api/stadiums/", self.stadium_data)
        self.assertEqual(stadium_response.status_code, 201)
        self.assertEqual(stadium_response.data["name"], "Piracanjuba")
        self.assertEqual(stadium_response.data["capacity"], 1000)

    def test_get_stadiums(self):
        stadium_response = self.client.get("/api/stadiums/")
        self.assertEqual(stadium_response.status_code, 200)

    def test_get_stadium(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        stadium_response = self.client.post("/api/stadiums/", self.stadium_data)
        stadium_id = stadium_response.data["id"]
        stadium = self.client.get(f"/api/stadiums/{stadium_id}/")
        self.assertEqual(stadium.status_code, 200)
        self.assertEqual(stadium.data["name"], "Piracanjuba")

    def test_update_stadium(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])
        stadium_response = self.client.post("/api/stadiums/", self.stadium_data)
        stadium_id = stadium_response.data["id"]
        stadium_update = self.client.patch(
            f"/api/stadiums/{stadium_id}/", {"name": "update-stadium"}
        )
        self.assertEqual(stadium_update.status_code, 200)
        self.assertEqual(stadium_update.data["name"], "update-stadium")

    def test_delete_stadium(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])
        stadium_response = self.client.post("/api/stadiums/", self.stadium_data)
        stadium_id = stadium_response.data["id"]
        stadium_delete = self.client.delete(f"/api/stadiums/{stadium_id}/")
        self.assertEqual(stadium_delete.status_code, 204)
