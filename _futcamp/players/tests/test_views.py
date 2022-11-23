from rest_framework.test import APITestCase

from users.models import User
from players.models import Player

from model_bakery import baker


class PlayerViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.player = {
            "name": "Gabriel Barbosa",
            "birthdate": "1996-10-14",
            "hometown": "Santos-SP",
            "biography": "Decidiu duas libertadores para o Flamengo",
            "number_of_goals": 200,
            "position": "Atacante",
            "shirt_number": 10,
        }

        cls.player_2 = {
            "name": "Gabriel Barbosa",
            "birthdate": "1996-10-14",
            "hometown": "Santos-SP",
            "biography": "Decidiu duas libertadores para o Flamengo",
            "number_of_goals": 200,
            "position": "Atacante",
            "shirt_number": 10,
        }

        cls.player_patch = {
            "name": "Pedro Guilherme",
            "shirt_number": 9,
        }

        cls.expected_keys = {
            "id",
            "name",
            "birthdate",
            "age",
            "hometown",
            "biography",
            "number_of_goals",
            "number_of_titles",
            "titles",
            "position",
            "shirt_number",
            "current_team",
        }

        cls.team = baker.make("teams.Team")

        cls.player_created = Player.objects.create(
            **cls.player,
            current_team=cls.team,
        )

        cls.normal_user_data = {
            "name": "guilhermina",
            "email": "guilhermina@mail.com",
            "password": "123456",
            "birthdate": "1999-09-09",
            "genre": "Feminino",
        }

        cls.superuser_data = {
            "name": "Adamastor",
            "email": "adamastor@mail.com",
            "password": "123456",
            "birthdate": "1999-09-09",
            "genre": "Masculino",
        }

        cls.superuser = User.objects.create_superuser(**cls.superuser_data)
        cls.normal_user = User.objects.create_user(**cls.normal_user_data)

    def test_create_player(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.post("/api/players/", self.player_2)

        response_keys = set(response.data.keys())

        self.assertEqual(response.status_code, 201)
        self.assertSetEqual(self.expected_keys, response_keys)

    def test_create_player_missing_keys(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.post("/api/players/", {})

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.data,
            {
                "name": ["This field is required."],
                "birthdate": ["This field is required."],
                "hometown": ["This field is required."],
                "biography": ["This field is required."],
                "number_of_goals": ["This field is required."],
                "shirt_number": ["This field is required."],
            },
        )

    def test_list_players(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        self.client.post("/api/players/", self.player)

        response = self.client.get("/api/players/")

        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_player(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        player = self.client.post("/api/players/", self.player)
        id = player.data["id"]

        response = self.client.get(f"/api/players/{id}/")

        response_keys = set(response.data.keys())

        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(self.expected_keys, response_keys)

    def test_retrieve_player_invalid_id(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.get("/api/players/777-777-777/")

        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.data)

    def test_update_player(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        player = self.client.post("/api/players/", self.player)
        id = player.data["id"]

        response = self.client.patch(
            f"/api/players/{id}/",
            self.player_patch,
        )

        response_keys = set(response.data.keys())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Pedro Guilherme")
        self.assertEqual(response.data["shirt_number"], 9)
        self.assertSetEqual(self.expected_keys, response_keys)

    def test_update_player_invalid_id(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.patch(
            f"/api/players/777-777-777/",
            self.player_patch,
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.data)

    def test_delete_player(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        player = self.client.post("/api/players/", self.player)
        id = player.data["id"]

        response = self.client.delete(f"/api/players/{id}/")

        self.assertEqual(response.status_code, 204)

    def test_delete_player_invalid_id(self):

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.delete(f"/api/players/777-777-777/")

        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.data)
