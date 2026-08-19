from datetime import datetime


def parse_date(value):
    if value is None:
        return None
    try:
        # Accept ISO format date or full datetime
        d = datetime.fromisoformat(value)
        return d.date()
    except Exception:
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except Exception:
            return None