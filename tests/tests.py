from django.test import TestCase


class MyTestCase(TestCase):
    def test_foo(self):
        self.assertEqual(True, True)
