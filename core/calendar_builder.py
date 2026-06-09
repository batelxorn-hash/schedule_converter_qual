from datetime import datetime

from core.models import ScheduleEvent


class CalendarBuilder:
    """
    Генерує iCalendar (.ics) файл із подій розкладу.
    """

    def __init__(self):
        self.events = []

    def add_events(self, events: list[ScheduleEvent]):
        """
        Додає список подій у календар.
        """
        self.events.extend(events)

    def build_ics(self) -> str:
        """
        Формує текст .ics файлу.
        """

        ics_content = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            "PRODID:-//Schedule Converter//UA Project//EN",

        ]

        for event in self.events:
            ics_content.extend(self._build_event(event))

        ics_content.append("END:VCALENDAR")

        return "\n".join(ics_content)

    def _build_event(self, event: ScheduleEvent) -> list[str]:

        start = self._format_datetime(event.start_datetime)
        end = self._format_datetime(event.end_datetime)

        uid = f"{event.subject}-{start}@schedule"

        vevent = [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTART;TZID=Europe/Kyiv:{start}",
            f"DTEND;TZID=Europe/Kyiv:{end}",
            f"SUMMARY:{event.subject}",
            "RRULE:FREQ=WEEKLY;COUNT=15"
        ]

        if event.teacher:
            vevent.append(
                f"DESCRIPTION:Викладач: {event.teacher}"
            )

        if event.room:
            vevent.append(
                f"LOCATION:{event.room}"
            )

        vevent.append("END:VEVENT")

        return vevent

    @staticmethod
    def _format_datetime(dt: datetime) -> str:
        """
        Форматує дату у формат iCalendar (UTC-like без Z).
        """

        return dt.strftime("%Y%m%dT%H%M%S")