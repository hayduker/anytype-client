from .template import Template
from .api import apiEndpoints


class Type:
    def __init__(self, name: str = ""):
        self._apiEndpoints: apiEndpoints | None = None
        self._all_templates = []
        self.type = ""
        self.space_id = ""
        self.id = ""
        self.name = ""
        self.icon = {}
        self.key = ""
        self.template_id = ""
        if name != "":
            self.set_template(name)

    def get_templates(
        self, offset: int = 0, limit: int = 100
    ) -> list[Template]:
        if self._apiEndpoints is None:
            raise Exception("You need to auth first")

        response_data = self._apiEndpoints.getTemplates(
            self.space_id, self.id, offset, limit
        )
        self._all_templates = []
        for data in response_data.get("data", []):
            new_template = Template()
            new_template._apiEndpoints = self._apiEndpoints
            for key, value in data.items():
                new_template.__dict__[key] = value
            self._all_templates.append(new_template)
        return self._all_templates

    def set_template(self, template_name: str) -> None:
        if len(self._all_templates) == 0:
            self.get_templates()

        found = False
        for template in self._all_templates:
            if template.name == template_name:
                found = True
                self.template_id = template.id
                return
        if not found:
            raise ValueError(
                f"Type '{self.name}' does not have "
                "a template named '{template_name}'"
            )

    def get_template(self, id: str) -> Template:
        if self._apiEndpoints is None:
            raise Exception("You need to auth first")
        response_data = self._apiEndpoints.getTemplate(
            self.space_id, self.id, id
        )
        results = []
        new_item = Template()
        new_item._apiEndpoints = self._apiEndpoints
        for data in response_data.get("data", []):
            for key, value in data.items():
                new_item.__dict__[key] = value
            results.append(new_item)
        return new_item

    def __repr__(self):
        if "emoji" in self.icon:
            return f"<Type(name={self.name}, icon={self.icon['emoji']})>"
        else:
            return f"<Type(name={self.name}, icon={self.icon['name']})>"
