from datetime import datetime, timedelta
from typing import Any


def generate_default_itinerary(start_date: datetime, end_date: datetime) -> list[dict[str, Any]]:
    """Create a default itinerary template for the trip duration"""
    if end_date < start_date:
        raise ValueError("end_date must be on or after start_date")

    itinerary = {}
    current_date = start_date

    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        itinerary[date_str] = {
            'activities': [],
            'meals': {
                'breakfast': {'time': '08:00', 'place': '', 'notes': ''},
                'lunch': {'time': '08:00', 'place': '', 'notes': ''},
                'dinner': {'time': '08:00', 'place': '', 'notes': ''}
            },
            'acommodation': {
                'name': '',
                'address': '',
                'check_in': '',
                'check_out': '',
                'confirmation': ''
            },
            'transportation': [],
            'notes': ''
        }
        current_date += timedelta(days=1)

    return itinerary
