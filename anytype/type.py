from .template import Template
from .api import apiEndpoints, APIWrapper
from .utils import requires_auth


class Type(APIWrapper):
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

    @requires_auth
    def get_templates(self, offset: int = 0, limit: int = 100) -> list[Template]:
        response = self._apiEndpoints.getTemplates(self.space_id, self.id, offset, limit)
        self._all_templates = [
            Template._from_api(self._apiEndpoints, data)
            for data in response.get("data", [])
        ]

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
                f"Type '{self.name}' does not have " "a template named '{template_name}'"
            )

    @requires_auth
    def get_template(self, id: str) -> Template:
        response = self._apiEndpoints.getTemplate(self.space_id, self.id, id)

        # TODO: This API response is unlike the rest, it returns a list for
        # "data" even though we're asking for info on a single template.
        # Bug in anytype-heart, or am I misunderstanding?
        datas = response.get("data", [])
        if len(datas) > 1:
            print(f"getTemplate response data has more than one entry: {response}")

        return Template._from_api(self._apiEndpoints, datas[0])

    @requires_auth
    def get_template(self, id: str) -> Template:
        response_data = self._apiEndpoints.getTemplate(self.space_id, self.id, id)

        template = Template()
        template._apiEndpoints = self._apiEndpoints
        for data in response_data.get("data", []):
            for key, value in data.items():
                template.__dict__[key] = value

        return template

    def __repr__(self):
        if "emoji" in self.icon:
            return f"<Type(name={self.name}, icon={self.icon['emoji']})>"
        else:
            return f"<Type(name={self.name}, icon={self.icon['name']})>"
