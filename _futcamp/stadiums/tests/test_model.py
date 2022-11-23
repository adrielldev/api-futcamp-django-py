from django.test import TestCase
from stadiums.models import Stadium


class StadiumModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.stadium_data = {
            "name": "Piracanjuba",
            "description": "Lugar onde o filho chora e a mãe não vê",
            "capacity": 1000,
            "localizations": "Recife",
            "area": 1000,
        }

        cls.stadium = Stadium.objects.create(**cls.stadium_data)

    def test_name_max_length(self):
        max_length = self.stadium._meta.get_field("name").max_length
        self.assertEquals(max_length, 255)

    def test_description_max_length(self):
        max_length = self.stadium._meta.get_field("description").max_length
        self.assertEquals(max_length, 500)

    def test_localizations_max_length(self):
        max_length = self.stadium._meta.get_field("localizations").max_length
        self.assertEquals(max_length, 255)
