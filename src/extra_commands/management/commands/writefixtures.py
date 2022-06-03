from django.core.management import BaseCommand

from extra_commands.utils import Excel2JsonFixtureWriter


class Command(BaseCommand):
    """A command to write Django JSON fixtures from Excel workbook."""

    help = "Creates JSON Django fixtures from the Microsoft Excel workbook."

    def add_arguments(self, parser):
        """Define the command arguments."""
        parser.add_argument(
            "workbook",
            type=str,
            help="Path to the source MS Excel workbook.",
        )
        parser.add_argument(
            "-a",
            "--apps",
            type=str,
            nargs="+",
            required=True,
            default=[],
            help="Labels of the apps.",
        )

    def handle(self, *args, **options):
        """Define what the command does."""
        Excel2JsonFixtureWriter(
            workbook=options["workbook"],
            apps=options["apps"],
        ).write_fixtures()
