from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScheduleEvent:
    """
    Модель одного заняття.
    """

    subject: str
    start_datetime: datetime
    end_datetime: datetime

    teacher: str = ""
    room: str = ""

    recurrence_type: str = "weekly"