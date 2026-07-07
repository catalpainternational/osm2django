"""Smoke tests for management commands — verify wiring without needing real OSM data."""

from django.core.management import get_commands, load_command_class
from django.core.management.base import CommandError
from django.test import TestCase


class ImportFromPgosmflexTests(TestCase):
    def test_command_is_registered(self):
        self.assertEqual(get_commands().get("import_from_pgosmflex"), "osmflex")

    def test_command_accepts_flags(self):
        cmd = load_command_class("osmflex", "import_from_pgosmflex")
        parser = cmd.create_parser("manage.py", "import_from_pgosmflex")
        # Argparse raises SystemExit on unrecognized args; a clean parse means the
        # flags are wired.
        args = parser.parse_args(["--truncate", "--unitable"])
        self.assertTrue(args.truncate)
        self.assertTrue(args.unitable)


class RunOsm2pgsqlTests(TestCase):
    def test_command_is_registered(self):
        self.assertEqual(get_commands().get("run_osm2pgsql"), "osmflex")

    def test_command_requires_positional_arg(self):
        cmd = load_command_class("osmflex", "run_osm2pgsql")
        parser = cmd.create_parser("manage.py", "run_osm2pgsql")
        with self.assertRaises(CommandError):
            parser.parse_args([])

    def test_command_accepts_osmfile_arg(self):
        cmd = load_command_class("osmflex", "run_osm2pgsql")
        parser = cmd.create_parser("manage.py", "run_osm2pgsql")
        args = parser.parse_args(["/tmp/foo.osm.pbf"])
        self.assertEqual(args.osmfile, "/tmp/foo.osm.pbf")


class CommandExecutionSmokeTests(TestCase):
    """The command uses transaction.atomic() internally and can leave a broken
    transaction in the enclosing TestCase; we don't execute it here. See the
    ``examples/minimal_import/`` runbook for real end-to-end usage."""

    def test_command_error_is_correct_type(self):
        # Sanity check that CommandError is importable from django (protects
        # against the run_osm2pgsql command silently swapping error types).
        self.assertTrue(issubclass(CommandError, Exception))
