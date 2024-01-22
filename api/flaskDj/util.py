from dateutil import parser


def is_valid_date(date_string):
    try:
        # Attempt to parse the date string
        return parser.parse(date_string).date()
    except ValueError:
        # If parsing fails, it's not a valid date
        return False
