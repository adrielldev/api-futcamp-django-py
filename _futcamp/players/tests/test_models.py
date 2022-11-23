from django.test import TestCase

from model_bakery import baker


class PlayerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.player_created = baker.make("players.Player")

    def test_name_max_length(self):
        max_length = self.player_created._meta.get_field("name").max_length

        self.assertEqual(max_length, 255)

    def test_hometown_max_length(self):
        max_length = self.player_created._meta.get_field("hometown").max_length

        self.assertEqual(max_length, 150)

    def test_position_max_length(self):
        max_length = self.player_created._meta.get_field("position").max_length

        self.assertEqual(max_length, 50)

    def test_current_team_null_blank(self):
        nullable = self.player_created._meta.get_field("current_team").null
        blankable = self.player_created._meta.get_field("current_team").blank

        self.assertEqual(nullable, True)
        self.assertEqual(blankable, True)
