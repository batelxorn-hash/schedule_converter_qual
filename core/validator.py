import re
from datetime import datetime


class ScheduleValidator:
    """
    Перевіряє коректність текстового розкладу.
    """

    TIME_REGEX = re.compile(r"(\d{1,2}[:.]\d{2})\s*-\s*(\d{1,2}[:.]\d{2})")

    def validate_line(self, line: str):

        if not line.strip():
            return []

        match = self.TIME_REGEX.search(line)

        if not match:
            return []  # дні і заголовки ігноруємо

        errors = []

        try:
            start = self._parse_time(match.group(1))
            end = self._parse_time(match.group(2))

            if start >= end:
                errors.append("Час початку >= часу закінчення")

        except Exception:
            errors.append("Помилка парсингу часу")

        return errors

    def _parse_time(self, t: str):
        return datetime.strptime(t.replace(".", ":"), "%H:%M").time()