from django.test import TestCase

from users.models import User
from teams.models import Team
from players.models import Player
from championships.models import Championship


class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_cadastro = {
            "name": "Xuxa Meneguel",
            "email": "xuxa@mail.com",
            "password": "ilarilarie",
            "birthdate": "1964-10-10",
            "genre": "Não Informado",
        }

        cls.user_xuxa = User.objects.create_user(**cls.user_cadastro)

    def test_atributs(self):
        name_max = self.user_xuxa._meta.get_field("name").max_length
        email_max = self.user_xuxa._meta.get_field("email").max_length
        name_unique = self.user_xuxa._meta.get_field("name").unique
        email_unique = self.user_xuxa._meta.get_field("email").unique

        self.assertEqual(name_max, 255)
        self.assertEqual(email_max, 255)
        self.assertEqual(name_unique, False)
        self.assertEqual(email_unique, True)

    def test_values_input(self):
        self.assertEqual(self.user_xuxa.name, self.user_cadastro["name"])
        self.assertEqual(self.user_xuxa.birthdate, self.user_cadastro["birthdate"])
