import os
import json

from .space import Space
from .object import Object
from .api import apiEndpoints


class Anytype:
    def __init__(self) -> None:
        self.app_name = ""
        self.space_id = ""
        self.token = ""
        self.app_key = ""
        self._apiEndpoints: apiEndpoints | None = None
        self._headers = {}

    def auth(self, force=False, callback=None) -> None:
        userdata = self._get_userdata_folder()
        anytoken = os.path.join(userdata, "any_token.json")

        if force and os.path.exists(anytoken):
            os.remove(anytoken)

        if self.app_name == "":
            self.app_name = "python-anytype-client"

        if os.path.exists(anytoken):
            with open(anytoken) as f:
                auth_json = json.load(f)
            self.token = auth_json.get("session_token")
            self.app_key = auth_json.get("app_key")
            if self._validate_token():
                return

        # Inicializa o client de API com o nome do app
        self._apiEndpoints = apiEndpoints()
        display_code_response = self._apiEndpoints.displayCode()
        challenge_id = display_code_response.get("challenge_id")

        if callback is None:
            api_four_digit_code = input("Enter the 4 digit code: ")
        else:
            api_four_digit_code = callback()

        token_response = self._apiEndpoints.getToken(challenge_id, api_four_digit_code)

        # Salva o token localmente
        with open(anytoken, "w") as file:
            json.dump(token_response, file, indent=4)

        self.token = token_response.get("session_token")
        self.app_key = token_response.get("app_key")
        self._validate_token()

    def _validate_token(self) -> bool:
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.app_key}",
        }
        self._apiEndpoints = apiEndpoints(self._headers)
        try:
            self._apiEndpoints.getSpaces(0, 1)
            return True
        except Exception:
            return False

    def _get_userdata_folder(self) -> str:
        userdata = os.path.join(os.path.expanduser("~"), ".anytype")
        if not os.path.exists(userdata):
            os.makedirs(userdata)
        if os.name == "nt":
            os.system(f"attrib +h {userdata}")
        return userdata

    def get_space(self, spaceId: str) -> Space:
        if self._apiEndpoints is None:
            raise Exception("You need to auth first")
        response_data = self._apiEndpoints.getSpace(spaceId)
        obj = Space()
        obj._apiEndpoints = self._apiEndpoints
        for key, value in response_data.get("object", {}).items():
            obj.__dict__[key] = value
        return obj

    def get_spaces(self, offset=0, limit=10) -> list[Space]:
        if self._apiEndpoints is None:
            raise Exception("You need to auth first")

        response = self._apiEndpoints.getSpaces(offset, limit)
        results = []
        for data in response.get("data", []):
            new_item = Space()
            new_item._apiEndpoints = self._apiEndpoints
            for key, value in data.items():
                new_item.__dict__[key] = value
            results.append(new_item)

        return results

    def create_space(self, name: str) -> Space:
        if self._apiEndpoints is None:
            raise Exception("You need to auth first")
        data = self._apiEndpoints.createSpace(name)
        new_space = Space()
        new_space._apiEndpoints = self._apiEndpoints
        for key, value in data["space"].items():
            new_space.__dict__[key] = value
        return new_space

    def global_search(self, query, offset=0, limit=10) -> list[Object]:
        if self._apiEndpoints is None:
            raise Exception("You need to auth first")
        response_data = self._apiEndpoints.globalSearch(query, offset, limit)
        results = []
        for data in response_data.get("data", []):
            new_item = Object()
            new_item._apiEndpoints = self._apiEndpoints
            for key, value in data.items():
                new_item.__dict__[key] = value
            results.append(new_item)
        return results
