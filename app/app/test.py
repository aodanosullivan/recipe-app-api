from django.test import TestCase

from app.calc import add

class CalcTests(TestCase):

    def test_add_numbers(self):
        """
        Test that 2 numbers are added together
        :return:
        """

        self.assertEqual(add(4, 6), 10)
