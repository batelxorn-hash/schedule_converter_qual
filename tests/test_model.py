from datetime import datetime
from core.models import ScheduleEvent


def test_event_creation():
    event = ScheduleEvent(
        subject="Програмування",
        start_datetime=datetime.now(),
        end_datetime=datetime.now()
    )

    assert event.subject == "Програмування"