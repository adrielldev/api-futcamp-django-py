from django.test import TestCase
from teams.models import Team

from model_bakery import baker


class TeamModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.coach = baker.make("coachs.Coach")
        cls.stadium = baker.make("stadiums.Stadium")
        cls.players = [baker.make("players.Player") for _ in range(5)]
        cls.team = baker.make(
            "teams.Team",
            coach=cls.coach,
            stadium=cls.stadium,
            players=cls.players,
        )

    def test_name_max_length(self):
        """Verifica a propriedade max_length de `name`"""

        expected = 255
        result = Team._meta.get_field("name").max_length
        msg = f"Verifique se a propriedade `max_length` de name foi definida como {expected}"

        self.assertEqual(expected, result, msg)

    def test_mascot_max_length(self):
        """Verifica a propriedade max_length de `mascot`"""

        expected = 150
        result = Team._meta.get_field("mascot").max_length
        msg = f"Verifique se a propriedade `max_length` de mascot foi definida como {expected}"

        self.assertEqual(expected, result, msg)

    def test_team_contain_unique_coach(self):
        """Verificando se o `team` possui apenas um `coach`"""

        msg = "Verifique se os valores do campo `coach` estão corretos"

        self.assertIs(self.coach, self.team.coach, msg)

    def test_team_contain_unique_stadium(self):
        """Verificando se o `team` possui apenas um `stadium`"""

        msg = "Verifique se os valores do campo `stadium` estão corretos"

        self.assertIs(self.stadium, self.team.stadium, msg)

    def test_team_contain_many_player(self):
        """Verificando se o `team` pode ter varios `player`"""

        msg = "Verifique se os valores do campo `players` estão corretos"

        for player in self.players:
            self.assertIn(player, self.team.players.all(), msg)
