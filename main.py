from datetime import datetime

from core.parser import ScheduleParser
from core.calendar_builder import CalendarBuilder


def main():
    print("=== Schedule Converter ===")

    # 1. Ініціалізація парсера
    parser = ScheduleParser("templates/default_schedule.json")

    # 2. Вхідний текст (поки вручну)
    text = """
    Понеділок
    08:30 - 10:05 Програмування
    10:25 - 12:00 Бази даних
    """

    # 3. Парсинг
    events = parser.parse(text, datetime(2026, 9, 1))

    print(f"Знайдено подій: {len(events)}")

    # 4. Побудова календаря
    builder = CalendarBuilder()
    builder.add_events(events)

    ics_content = builder.build_ics()

    # 5. Збереження у файл
    output_file = "schedule.ics"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(ics_content)

    print(f"Файл створено: {output_file}")


if __name__ == "__main__":
    main()