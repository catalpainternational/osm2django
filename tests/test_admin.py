"""Sanity check that every concrete osmflex model is registered in the admin site."""

from django.apps import apps
from django.contrib import admin
from django.test import TestCase


class AdminRegistrationTests(TestCase):
    def test_all_concrete_models_registered(self):
        expected = {m for m in apps.get_app_config("osmflex").get_models() if not m._meta.abstract}
        registered = set(admin.site._registry.keys())
        missing = expected - registered
        self.assertFalse(missing, f"Not registered in admin: {sorted(m.__name__ for m in missing)}")
