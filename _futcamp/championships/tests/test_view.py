from rest_framework.test import APITestCase
from django.utils.crypto import get_random_string

from championships.models import Championship
from users.models import User
from teams.models import Team


class ChampionshipsViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teams = [
            Team.objects.create(
                name=get_random_string(8),
                mascot=get_random_string(5),
                team_foundation_year="1996-09-09",
            )
            for _ in range(2)
        ]
        cls.championship_data = {
            "name": "garcia",
            "description": "awsgfasdverfw dffwg ffegfegdh",
            "initial_date": "2002-03-04",
            "end_date": "2003-03-04",
            "award": "9.2",
        }
        cls.championship_update_data = {"name": "garcia jr", "award": "109.2"}
        cls.championship = Championship.objects.create(**cls.championship_data)
        cls.championship.teams.set(cls.teams)
        cls.superuser_data = {
            "name": "Adamastor",
            "email": "adamastor@mail.com",
            "password": "123456",
            "birthdate": "1999-09-09",
            "genre": "Masculino",
        }
        cls.superuser = User.objects.create_superuser(**cls.superuser_data)

    def test_create_championship(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        championship_data = {
            "name": "garcia chalanger plus ultra jorge",
            "description": "Torneio do garcia",
            "initial_date": "2001-01-01",
            "end_date": "2002-02-02",
            "award": 0.23,
            "teams": [],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        championship_response = self.client.post(
            "/api/championships/", championship_data
        )

        self.assertEqual(championship_response.status_code, 201)
        self.assertEqual(
            championship_response.data["award"], championship_data["award"]
        )
        self.assertEqual(championship_response.data["name"], championship_data["name"])
        self.assertEqual(
            championship_response.data["description"], championship_data["description"]
        )
        self.assertEqual(
            championship_response.data["initial_date"],
            championship_data["initial_date"],
        )
        self.assertEqual(
            championship_response.data["end_date"], championship_data["end_date"]
        )

    def test_get_championships(self):
        response = self.client.get("/api/championships/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_championship(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        championship_response = self.client.get(
            f"/api/championships/{self.championship.id}/"
        )

        self.assertEqual(championship_response.status_code, 200)
        self.assertEqual(championship_response.data["award"], 9.2)
        self.assertEqual(championship_response.data["name"], "garcia")
        self.assertEqual(
            championship_response.data["description"], "awsgfasdverfw dffwg ffegfegdh"
        )

    def test_update_championships(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        championship_response = self.client.patch(
            f"/api/championships/{self.championship.id}/", self.championship_update_data
        )

        self.assertEqual(championship_response.status_code, 200)
        self.assertEqual(
            championship_response.data["name"], self.championship_update_data["name"]
        )

    def test_delete_championship(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        championship_response = self.client.delete(
            f"/api/championships/{self.championship.id}/"
        )

        self.assertEqual(championship_response.status_code, 204)
