from core.template_loader import TemplateLoader

template = TemplateLoader.load_template(
    "templates/default_schedule.json"
)

print(template)