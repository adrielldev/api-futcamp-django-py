from rest_framework.test import APITestCase
from coachs.models import Coach
from users.models import User


class CoachViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.coach_data = {
            "name": "teste",
            "birthdate": "2000-08-15",
            "biography": "ajkfasklfklas",
            "hometown": "recife",
        }
        cls.coach = Coach.objects.create(**cls.coach_data)

        cls.superuser_data = {
            "name": "Adamastor",
            "email": "adamastor@mail.com",
            "password": "123456",
            "birthdate": "1999-09-09",
            "genre": "Masculino",
        }
        cls.superuser = User.objects.create_superuser(**cls.superuser_data)

    def test_create_coach(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        coach_response = self.client.post("/api/coachs/", self.coach_data)
        self.assertEqual(coach_response.status_code, 201)
        self.assertEqual(coach_response.data["name"], "teste")
        self.assertEqual(coach_response.data["number_of_titles"], 0)

    def test_get_coachs(self):
        response = self.client.get("/api/coachs/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_get_coach(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        coach_response = self.client.post("/api/coachs/", self.coach_data)

        coach_id = coach_response.data["id"]

        coach = self.client.get(f"/api/coachs/{coach_id}/")

        self.assertEqual(coach.status_code, 200)
        self.assertEqual(coach.data["name"], "teste")

    def test_update_coachs(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        coach_response = self.client.post("/api/coachs/", self.coach_data)
        coach_id = coach_response.data["id"]
        coach_update = self.client.patch(
            f"/api/coachs/{coach_id}/", {"name": "update-coach"}
        )
        self.assertEqual(coach_update.status_code, 200)
        self.assertEqual(coach_update.data["name"], "update-coach")

    def test_delete_coach(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        coach_response = self.client.post("/api/coachs/", self.coach_data)
        coach_id = coach_response.data["id"]
        coach_delete = self.client.delete(f"/api/coachs/{coach_id}/")
        self.assertEqual(coach_delete.status_code, 204)
