import tkinter as tk
from datetime import datetime
from tkinter import messagebox, scrolledtext
from tkinter import filedialog
import os
import subprocess
from core.calendar_builder import CalendarBuilder
from core.parser import ScheduleParser
from core.file_loader import FileLoader
from core.validator import ScheduleValidator
from core.logger import logger
from core.conflict_detector import ConflictDetector

class ScheduleApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Schedule Converter")
        self.root.geometry("700x500")

        # Заголовок
        self.label = tk.Label(root, text="Встав розклад:", font=("Arial", 12))
        self.label.pack(pady=5)

        # Текстове поле
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15)
        self.text_area.focus_set()
        self.text_area.pack(pady=5)

        self.date_label = tk.Label(
            root,
            text="Дата початку семестру (РРРР-ММ-ДД)"
        )

        self.date_label.pack()

        self.date_entry = tk.Entry(root)

        self.date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        self.date_entry.pack()

        # Кнопка завантаження файлу
        self.load_button = tk.Button(
            root,
            text="Завантажити розклад з файлу",
            command=self.load_file
        )
        self.load_button.pack(pady=5)

        # Кнопка відкриття результату
        self.open_button = tk.Button(
            root,
            text="Відкрити .ics файл",
            command=self.open_calendar
        )
        self.open_button.pack(pady=5)

        self.loaded_text = ""
        self.output_file = "schedule.ics"

        # Кнопка
        self.button = tk.Button(
            root,
            text="Згенерувати календар (.ics)",
            command=self.generate_calendar
        )
        self.button.pack(pady=10)

        tk.Button(root, text="Вставити", command=self.paste_text).pack()

        # Статус
        self.status = tk.Label(root, text="", fg="green")
        self.status.pack(pady=5)

        # Парсер
        import os

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        template_path = (os.path.join
                         (BASE_DIR, "templates", "default_schedule.json"))

        self.parser = ScheduleParser(template_path)

        self.validator = ScheduleValidator()

    def open_calendar(self):
        if not os.path.exists(self.output_file):
            messagebox.showerror("Помилка", "Файл ще не створено")
            return

        try:
            if os.name == "nt":
                os.startfile(self.output_file)
            else:
                subprocess.call(["open", self.output_file])

        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def paste_text(self):
        try:
            text = self.root.clipboard_get()
            self.text_area.insert(tk.END, text)
        except:
            messagebox.showerror("Помилка", "Буфер обміну порожній")

    def generate_calendar(self):
        try:
            text = self.text_area.get("1.0", tk.END).strip()

            if not text:
                messagebox.showerror("Помилка", "Встав розклад!")
                return

            for line in text.splitlines():

                errors = self.validator.validate_line(line)

                if errors:
                    messagebox.showerror(
                        "Помилка у розкладі",
                        f"Рядок: {line}\n" + "\n".join(errors)
                    )

                    logger.error(
                        f"Помилка валідації: {line} -> {errors}"
                    )

                    return

            # Парсинг
            semester_start = datetime.strptime(
                self.date_entry.get(),
                "%Y-%m-%d"
            )

            events = self.parser.parse(
                text,
                semester_start
            )

            if not events:
                messagebox.showerror(
                    "Помилка",
                    "Не вдалося розпізнати розклад"
                )
                return

            conflicts = ConflictDetector.find_conflicts(events)

            if conflicts:
                text_conflicts = "\n".join(
                    f"{a} ↔ {b}"
                    for a, b in conflicts
                )

                messagebox.showwarning(
                    "Конфлікти",
                    f"Виявлено конфлікти:\n\n{text_conflicts}"
                )

            # Побудова календаря
            builder = CalendarBuilder()
            builder.add_events(events)

            ics_content = builder.build_ics()

            # Збереження файлу
            save_path = filedialog.asksaveasfilename(
                defaultextension=".ics",
                filetypes=[
                    ("iCalendar", "*.ics")
                ]
            )

            if not save_path:
                return

            with open(
                    save_path,
                    "w",
                    encoding="utf-8"
            ) as file:

                file.write(ics_content)

            self.output_file = save_path

            logger.info(
                f"Створено файл {self.output_file}"
            )

            self.status.config(text=f"Файл створено: {self.output_file}")
            messagebox.showinfo("Готово", "Календар успішно створено!")


        except Exception as e:

            logger.error(str(e))

            messagebox.showerror(
                "Помилка",
                str(e)
            )

    def load_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("All supported", "*.txt *.csv *.xlsx *.pdf"),
                ("Text", "*.txt"),
                ("CSV", "*.csv"),
                ("Excel", "*.xlsx"),
                ("PDF", "*.pdf")
            ]
        )

        if not file_path:
            return

        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

        elif file_path.endswith(".csv"):
            content = FileLoader.load_csv(file_path)

        elif file_path.endswith(".xlsx"):
            content = FileLoader.load_excel(file_path)

        elif file_path.endswith(".pdf"):
            content = FileLoader.load_pdf(file_path)

        else:
            messagebox.showerror("Помилка", "Непідтримуваний формат")
            return

        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, content)

        self.status.config(text="Файл завантажено")

def run_app():
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()