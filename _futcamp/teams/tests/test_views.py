from rest_framework.test import APITestCase
from rest_framework.views import status

from model_bakery import baker
from users.models import User
from teams.models import Team


class TeamViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.coach = baker.make("coachs.Coach")
        cls.stadium = baker.make("stadiums.Stadium")
        cls.players = [baker.make("players.Player") for _ in range(5)]
        cls.team_data = {
            "name": "Abacoteam",
            "mascot": "Abacate",
            "team_foundation_year": "1993-09-09",
            "coach": cls.coach,
            "stadium": cls.stadium,
        }
        cls.team = Team.objects.create(**cls.team_data)
        cls.team_update_data = {"name": "Itaquaquecetuba", "mascot": "Capivara"}
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

        cls.expected_keys = {
            "id",
            "name",
            "mascot",
            "number_of_players",
            "number_of_titles",
            "team_foundation_year",
            "updated_at",
            "titles",
            "players",
            "coach",
            "stadium",
        }

    def test_create_team_empty_body(self):
        """Não deve ser capaz de criar um novo `team` caso o corpo da requisição esteja vazio"""

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.post("/api/teams/", {})

        expected_status = status.HTTP_400_BAD_REQUEST
        expected_keys = {
            "name",
            "mascot",
            "team_foundation_year",
        }

        result_status = response.status_code
        result_keys = set(response.data.keys())

        msg_status = "O status code recebido esta diferente do esperado"

        self.assertEqual(expected_status, result_status, msg_status)
        self.assertSetEqual(expected_keys, result_keys)

    def test_create_team_with_normal_user(self):
        """Não deve ser capaz de criar um novo `team` com um usuário comum"""

        login_data = {
            "email": self.normal_user_data["email"],
            "password": self.normal_user_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.post("/api/teams/", self.team_data)

        expected_status = status.HTTP_403_FORBIDDEN
        expected_key = {"detail"}

        result_status = response.status_code
        result_key = set(response.data.keys())

        msg_status = "O status code recebido esta diferente do esperado"

        self.assertEqual(expected_status, result_status, msg_status)
        self.assertSetEqual(expected_key, result_key)

    def test_create_team_with_superuser(self):
        """Deve ser capaz de criar um novo `team` com um superusuario"""

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }
        team_data = {
            "name": "Abacoteam o retorno",
            "mascot": "Abacatron",
            "team_foundation_year": "1996-09-09",
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.post("/api/teams/", team_data)

        expected_status = status.HTTP_201_CREATED

        result_status = response.status_code
        result_keys = set(response.data.keys())

        msg_status = "O status code recebido esta diferente do esperado"

        self.assertEqual(expected_status, result_status, msg_status)
        self.assertSetEqual(self.expected_keys, result_keys)

    def test_list_teams_with_superuser(self):
        """Usuário do tipo superuser deve ser capaz de listar todos os times"""

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.get("/api/teams/")

        expected_status = status.HTTP_200_OK
        expected_keys = {"count", "next", "previous", "results"}
        expected_length = 1

        result_status = response.status_code
        result_keys = set(response.data.keys())
        result_length = len(response.data["results"])

        msg_status = "O status code recebido esta diferente do esperado"

        self.assertEqual(expected_status, result_status, msg_status)
        self.assertSetEqual(expected_keys, result_keys)
        self.assertEqual(expected_length, result_length)

    def test_list_teams_with_normal_user(self):
        """Usuário normal deve ser capaz de listr todos os times"""

        login_data = {
            "email": self.normal_user_data["email"],
            "password": self.normal_user_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.get("/api/teams/")

        expected_status = status.HTTP_200_OK
        expected_keys = {"count", "next", "previous", "results"}
        expected_length = 1

        result_status = response.status_code
        result_keys = set(response.data.keys())
        result_length = len(response.data["results"])

        msg_status = "O status code recebido esta diferente do esperado"

        self.assertEqual(expected_status, result_status, msg_status)
        self.assertSetEqual(expected_keys, result_keys)
        self.assertEqual(expected_length, result_length)

    def test_retrieve_team_with_superuser(self):
        """Usuário do tipo superuser deve ser capaz buscar um `team` por id"""

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.get(f"/api/teams/{self.team.id}/")

        expected_status = status.HTTP_200_OK

        result_status = response.status_code
        result_keys = set(response.data.keys())

        msg_status = "O status code recebido esta diferente do esperado"

        self.assertEqual(expected_status, result_status, msg_status)
        self.assertSetEqual(self.expected_keys, result_keys)

    def test_retrieve_team_with_normal_user(self):
        """Usuário normal deve ser capaz buscar um `team` por id"""

        login_data = {
            "email": self.normal_user_data["email"],
            "password": self.normal_user_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.get(f"/api/teams/{self.team.id}/")

        expected_status = status.HTTP_200_OK

        result_status = response.status_code
        result_keys = set(response.data.keys())

        msg_status = "O status code recebido esta diferente do esperado"

        self.assertEqual(expected_status, result_status, msg_status)
        self.assertSetEqual(self.expected_keys, result_keys)

    def test_update_team_with_superuser(self):
        """Usuário do tipo superuser deve ser capaz de atualizar os dados de um `team`"""

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.patch(
            f"/api/teams/{self.team.id}/", self.team_update_data
        )

        expected_status = status.HTTP_200_OK

        result_status = response.status_code
        result_keys = set(response.data.keys())

        msg_status = "O status code recebido esta diferente do esperado"

        self.assertEqual(expected_status, result_status, msg_status)
        self.assertSetEqual(self.expected_keys, result_keys)

    def test_update_team_with_normal_user(self):
        """Usuário normal não deve ser capaz de atualizar os dados de um `team`"""

        login_data = {
            "email": self.normal_user_data["email"],
            "password": self.normal_user_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.patch(
            f"/api/teams/{self.team.id}/", self.team_update_data
        )

        expected_status = status.HTTP_403_FORBIDDEN
        expected_keys = {"detail"}

        result_status = response.status_code
        result_keys = set(response.data.keys())

        msg_status = "O status code recebido esta diferente do esperado"

        self.assertEqual(expected_status, result_status, msg_status)
        self.assertSetEqual(expected_keys, result_keys)

    def test_delete_team_with_superuser(self):
        """Usuário do tipo superuser deve ser capaz de deletar um `team`"""

        login_data = {
            "email": self.superuser_data["email"],
            "password": self.superuser_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.delete(f"/api/teams/{self.team.id}/")

        expected_status = status.HTTP_204_NO_CONTENT
        result_status = response.status_code
        msg_status = "O status code recebido esta diferente do esperado"

        self.assertEqual(expected_status, result_status, msg_status)

    def test_delete_team_with_normal_user(self):
        """Usuário normal não deve ser capaz de deletar um `team`"""

        login_data = {
            "email": self.normal_user_data["email"],
            "password": self.normal_user_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.delete(f"/api/teams/{self.team.id}/")

        expected_status = status.HTTP_403_FORBIDDEN
        expected_keys = {"detail"}

        result_status = response.status_code
        result_keys = set(response.data.keys())

        msg_status = "O status code recebido esta diferente do esperado"

        self.assertEqual(expected_status, result_status, msg_status)
        self.assertSetEqual(expected_keys, result_keys)
