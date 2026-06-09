from datetime import datetime
from core.models import ScheduleEvent
from core.calendar_builder import CalendarBuilder


def test_calendar_builder():
    event = ScheduleEvent(
        subject="Програмування",
        start_datetime=datetime(2026, 9, 1, 8, 30),
        end_datetime=datetime(2026, 9, 1, 10, 5),
        teacher="Іван Петренко",
        room="101"
    )

    builder = CalendarBuilder()
    builder.add_events([event])

    ics = builder.build_ics()

    assert "BEGIN:VCALENDAR" in ics
    assert "BEGIN:VEVENT" in ics
    assert "Програмування" in ics
    assert "LOCATION:101" in ics