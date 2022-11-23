from django.test import TestCase
from coachs.models import Coach


class CoachModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.coach_data = {
            "name": "teste",
            "birthdate": "2000-08-15",

            "biography": "ajkfasklfklas",

            "hometown": "recife",

        }

        cls.coach = Coach.objects.create(**cls.coach_data)

    def test_name_max_length(self):
        max_length = self.coach._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_biography_max_length(self):
        max_length = self.coach._meta.get_field("biography").max_length
        self.assertEqual(max_length, 500)

    def test_hometown_max_length(self):
        max_length = self.coach._meta.get_field("hometown").max_length
        self.assertEqual(max_length, 50)
