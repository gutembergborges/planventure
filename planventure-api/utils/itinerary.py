from datetime import date, timedelta
from typing import Any


def generate_default_itinerary(
    destination: str,
    start_date: date,
    end_date: date,
) -> list[dict[str, Any]]:
    """Create an empty, dated itinerary template for a trip."""
    if end_date < start_date:
        raise ValueError("end_date must be on or after start_date")

    itinerary = []
    current_date = start_date
    day_number = 1

    while current_date <= end_date:
        itinerary.append({
            "day": day_number,
            "date": current_date.isoformat(),
            "destination": destination,
            "activities": [],
        })
        current_date += timedelta(days=1)
        day_number += 1

    return itinerary
