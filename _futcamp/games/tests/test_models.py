from django.test import TestCase

from model_bakery import baker


class GameModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.championship = baker.make("championships.Championship")

        cls.game = baker.make(
            "games.Game",
            championship=cls.championship,
        )

    def test_result_max_length(self):
        max_length = self.game._meta.get_field("result").max_length

        self.assertEqual(max_length, 150)

    def test_round_max_length(self):
        max_length = self.game._meta.get_field("round").max_length

        self.assertEqual(max_length, 150)
