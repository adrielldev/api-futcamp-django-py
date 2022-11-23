from django.test import TestCase
from championships.models import Championship


class ChampionshipsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.championships_data = {
            "name": "champions",
            "description": "new description",
            "initial_date": "2003-1-01",
            "end_date": "2003-02-03",
            "award": 9.2,
        }

        cls.championships = Championship.objects.create(**cls.championships_data)

    def test_name_max_length(self):
        max_length = self.championships._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)
