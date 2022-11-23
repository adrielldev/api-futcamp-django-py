from django.test import TestCase
from titles.models import Title


class TitleModelTest(TestCase):
    def test_name_max_length(self):
        """Verifica a propriedade max_length de `name`"""

        expected = 255
        result = Title._meta.get_field("name").max_length
        msg = f"Verifique se a propriedade `max_length` de name foi definida como {expected}"

        self.assertEqual(expected, result, msg)
