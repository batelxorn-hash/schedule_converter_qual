import json


class TemplateLoader:

    @staticmethod
    def load_template(path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)