import re
from datetime import datetime, timedelta

from core.models import ScheduleEvent
from core.template_loader import TemplateLoader


class ScheduleParser:

    def __init__(self, template_path):
        self.template = TemplateLoader.load_template(template_path)

        self.time_pattern = re.compile(
            self.template["time_pattern"]
        )

        self.days = self.template["days"]

    def parse(self, text, semester_start):

        events = []
        current_day_index = 0

        lines = text.split("\n")

        for line in lines:
            line = line.strip()

            if not line:
                continue

            # визначення дня
            for idx, day in enumerate(self.days):
                if line.lower() == day.lower():
                    current_day_index = idx
                    continue

            # пошук часу
            match = self.time_pattern.search(line)

            if not match:
                continue

            event = self._create_event(
                line,
                match,
                current_day_index,
                semester_start
            )

            events.append(event)

        return events

    def _create_event(
            self,
            line,
            match,
            day_index,
            semester_start
    ):

        start_time_str = match.group(1)
        end_time_str = match.group(2)

        subject = line[match.end():].strip()

        event_date = semester_start + timedelta(days=day_index)

        start_time = datetime.strptime(
            start_time_str.replace(".", ":"),
            "%H:%M"
        ).time()

        end_time = datetime.strptime(
            end_time_str.replace(".", ":"),
            "%H:%M"
        ).time()

        start_datetime = datetime.combine(
            event_date,
            start_time
        )

        end_datetime = datetime.combine(
            event_date,
            end_time
        )

        return ScheduleEvent(
            subject=subject,
            start_datetime=start_datetime,
            end_datetime=end_datetime
        )