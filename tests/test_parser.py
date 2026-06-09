from datetime import datetime

from core.parser import ScheduleParser


def test_parser():

    parser = ScheduleParser(
        "templates/default_schedule.json"
    )

    text = """
    Понеділок
    08:30 - 10:05 Програмування
    """

    events = parser.parse(
        text,
        datetime(2026, 9, 1)
    )

    assert len(events) == 1