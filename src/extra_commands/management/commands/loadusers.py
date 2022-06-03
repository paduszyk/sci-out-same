from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db import IntegrityError

import pandas as pd

# User fields

USER_FIELDS = [
    {
        "name": field[0],
        "required": field[1],
        "default": field[2] if len(field) > 2 else None,
    }
    for field in [
        ("id", True),
        ("username", True),
        ("password", True),
        ("email", False, ""),
        ("is_staff", False, False),
        ("is_superuser", False, False),
        ("first_name", False, ""),
        ("last_name", False, ""),
        ("sex", False, ""),
    ]
]


class Command(BaseCommand):
    """A command for bulk create/update of users from Excel workbook."""

    help = (
        "Creates or updates users based on the data saved in"
        "the Microsoft Excel workbook."
    )

    def add_arguments(self, parser):
        """Define the command arguments."""
        parser.add_argument(
            "workbook",
            type=str,
            help="Path to the source MS Excel workbook.",
        )
        parser.add_argument(
            "-s",
            "--sheet",
            nargs=1,
            type=str,
            required=False,
            default=get_user_model()._meta.label_lower,
            help=(
                "Name of the sheet containing the user data."
                " Default for the current project is "
                f"'{get_user_model()._meta.label_lower}'."
            ),
        )

    def handle(self, *args, **options):
        """Define what does the command do."""
        # Read the arguments
        workbook_path = options["workbook"]
        sheet = options["sheet"]

        # If the workbook has more than a single sheet, check if it also
        # has the sheet specified as the function parameter.
        workbook_sheets = pd.ExcelFile(workbook_path).sheet_names

        if len(workbook_sheets) > 1:
            if sheet not in workbook_sheets:
                raise ValueError(
                    f"Sheet '{sheet}' not found in " f"the workbook '{workbook_path}'."
                )
        else:
            # The only sheet is taken as the user-data sheet
            sheet = workbook_sheets[0]

        # Read the sheet from the workbook
        users = pd.read_excel(workbook_path, sheet_name=sheet, dtype="object")

        # Get the user's required fields
        fields = [field["name"] for field in USER_FIELDS]

        # Extract only the required data
        try:
            users = users[fields]
        except KeyError:
            raise KeyError(
                "The following columns are missing in the data sheet "
                "'{}' of workbook '{}': {}.".format(
                    sheet,
                    workbook_path,
                    ", ".join([field for field in fields if field not in users]),
                )
            )

        # Required fields
        required_fields = [field["name"] for field in USER_FIELDS if field["required"]]

        # Username and password are the required fields for each user
        if users[required_fields].isnull().values.any():
            raise ValueError(
                "The following fields has to be specified for"
                f"all the users: {', '.join(required_fields)}."
            )

        # Handle NaN or empty values in the remaining columns
        for field in USER_FIELDS:
            if field["default"] is not None and not field["required"]:
                users[field["name"]] = users[field["name"]].fillna(field["default"])

        # Create and/or update the users
        for _, user in users.iterrows():
            user = user.to_dict()

            try:
                get_user_model().objects.create_user(**user)
            except IntegrityError:
                self.stdout.write(
                    self.style.ERROR(
                        f"Problems occurred when creating user "
                        f"'{user['username']}'. Check whether it is "
                        "already saved in the database."
                    )
                )
