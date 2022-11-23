from rest_framework.test import APITestCase

from users.models import User
from games.models import Game

from model_bakery import baker


class GameViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.stadium = baker.make("stadiums.Stadium")
        cls.championship = baker.make("championships.Championship")
        cls.team_home = baker.make("teams.Team")
        cls.team_away = baker.make("teams.Team")
        cls.game_data = {
            "date": "2022-08-30 20:00:00",
            "result": "2x1",
            "round": 1,
            "stadium": cls.stadium,
            "championship": cls.championship,
        }
        cls.game = Game.objects.create(**cls.game_data)
        cls.game.teams.set(
            [
                str(cls.team_home.id),
                str(cls.team_away.id),
            ]
        )
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
            "date",
            "result",
            "round",
            "stadium",
            "championship",
            "teams",
        }

    # def test_create_game(self):
    #     login_data = {
    #         "email": self.superuser_data["email"],
    #         "password": self.superuser_data["password"],
    #     }
    #     login = self.client.post("/api/login/", login_data)
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

    #     game_data = {
    #         "date": "2022-08-30 20:00:00",
    #         "result": "2x1",
    #         "round": 1,
    #         "stadium": str(self.stadium.id),
    #         "championship": str(self.championship.id),
    #         "teams": [
    #             str(self.team_home.id),
    #             str(self.team_away.id),
    #         ],
    #     }
    #     response = self.client.post("/api/games/", game_data)

    #     response_keys = set(response.data.keys())

    #     self.assertEqual(response.status_code, 201)
    #     self.assertSetEqual(self.expected_keys, response_keys)

    def test_list_games(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.get("/api/games/")

        expected_keys = {"count", "results", "next", "previous"}
        response_keys = set(response.data.keys())

        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(expected_keys, response_keys)

    def test_retrieve_game(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.get(f"/api/games/{self.game.id}/")

        response_keys = set(response.data.keys())

        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(self.expected_keys, response_keys)

    def test_list_games_for_championships(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.get(f"/api/games/?championship={self.championship.id}")

        expected_keys = {"count", "results", "next", "previous"}
        response_keys = set(response.data.keys())

        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(expected_keys, response_keys)

    def test_list_games_for_championship_games(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.get(
            f"/api/games/?championship={self.championship.id}&round={self.game.round}"
        )

        expected_keys = {"count", "results", "next", "previous"}
        response_keys = set(response.data.keys())

        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(expected_keys, response_keys)

    def test_list_games_for_stadiums(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.get(f"/api/games/?stadium={self.stadium.id}")

        expected_keys = {"count", "results", "next", "previous"}
        response_keys = set(response.data.keys())

        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(expected_keys, response_keys)

    def test_list_games_for_team(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.get(f"/api/games/?teams={self.team_home.id}")

        expected_keys = {"count", "results", "next", "previous"}
        response_keys = set(response.data.keys())

        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(expected_keys, response_keys)

    def test_list_games_for_day(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.get(f"/api/games/?date={self.game.date}")

        expected_keys = {"count", "results", "next", "previous"}
        response_keys = set(response.data.keys())

        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(expected_keys, response_keys)

    def test_update_game(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.patch(
            f"/api/games/{self.game.id}/", {"date": "2022-12-31 00:00:00"}
        )

        response_keys = set(response.data.keys())

        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(self.expected_keys, response_keys)

    def test_delete_game(self):
        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.delete(f"/api/games/{self.game.id}/")

        self.assertEqual(response.status_code, 204)
