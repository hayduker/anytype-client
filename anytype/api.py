import requests
from urllib.parse import urlencode
from datetime import datetime
from typing import TypeVar, Type


MIN_REQUIRED_VERSION = datetime(2025, 3, 17).date()
API_CONFIG = {
    "apiUrl": "http://localhost:31009/v1",
    "apiAppName": "PythonClient",
}


class ResponseHasError(Exception):
    """Custom exception for API errors."""

    def __init__(self, response):
        self.status_code = response.status_code
        if self.status_code != 200:
            raise ValueError(response.json()["error"]["message"])


class apiEndpoints:
    def __init__(self, headers: dict = {}):
        self.api_url = API_CONFIG["apiUrl"].rstrip("/")
        self.app_name = API_CONFIG["apiAppName"]
        self.headers = headers

    def _request(self, method, path, params=None, data=None):
        url = f"{self.api_url}{path}"
        if params:
            url += "?" + urlencode(params)
        response = requests.request(method, url, headers=self.headers, json=data)

        version_str = response.headers.get("Anytype-Version")
        if version_str:
            version_date = datetime.strptime(version_str, "%Y-%m-%d").date()

            if version_date < MIN_REQUIRED_VERSION:
                print("❌ Version is too old:", version_date)
        else:
            raise ValueError("Anytype-Version header not found, probably anytype is too old")

        ResponseHasError(response)
        return response.json()

    # --- auth ---
    def displayCode(self):
        return self._request("POST", "/auth/display_code", params={"app_name": self.app_name})

    def getToken(self, challengeId: str, code: str):
        return self._request(
            "POST",
            "/auth/token",
            params={"challenge_id": challengeId, "code": code},
        )

    # --- export ---
    def getExport(self, spaceId: str, objectId: str, format: str):
        return self._request("GET", f"/spaces/{spaceId}/objects/{objectId}/{format}")

    # --- lists ---
    def getListViews(self, spaceId: str, listId: str, offset: int, limit: int):
        options = {"offset": offset, "limit": limit}
        return self._request("GET", f"/spaces/{spaceId}/lists/{listId}/views", params=options)

    def getObjectsInList(self, spaceId: str, listId: str, viewId: str, offset: int, limit: int):
        options = {"offset": offset, "limit": limit}
        return self._request(
            "GET",
            f"/spaces/{spaceId}/lists/{listId}/{viewId}/objects",
            params=options,
        )

    def addObjectsToList(self, spaceId: str, listId: str, object_ids: list[str]):
        return self._request("POST", f"/spaces/{spaceId}/lists/{listId}/objects", data=object_ids)

    def deleteObjectsFromList(self, spaceId: str, listId: str, objectId: str):
        return self._request("DELETE", f"/spaces/{spaceId}/lists/{listId}/objects/{objectId}")

    # --- objects ---
    def createObject(self, spaceId: str, data: dict):
        return self._request("POST", f"/spaces/{spaceId}/objects", data=data)

    def deleteObject(self, spaceId: str, objectId: str):
        return self._request("DELETE", f"/spaces/{spaceId}/objects/{objectId}")

    def getObject(self, spaceId: str, objectId: str):
        return self._request("GET", f"/spaces/{spaceId}/objects/{objectId}")

    def getObjects(self, spaceId: str, offset=0, limit=10):
        options = {"offset": offset, "limit": limit}
        return self._request("GET", f"/spaces/{spaceId}/objects", params=options)

    # --- search ---
    def globalSearch(self, query: str = "", offset=0, limit=10):
        options = {"offset": offset, "limit": limit}
        payload = {"query": query}
        return self._request("POST", "/search", params=options, data=payload)

    def search(self, spaceId: str, query: str, offset: int = 0, limit: int = 10):
        options = {"offset": offset, "limit": limit}
        payload = {"query": query}
        return self._request("POST", f"/spaces/{spaceId}/search", params=options, data=payload)

    # --- spaces ---
    def createSpace(self, name):
        data = {"name": name}
        return self._request("POST", "/spaces", data=data)

    def getSpace(self, spaceId: str):
        return self._request("GET", f"/spaces/{spaceId}")

    def getSpaces(self, offset=0, limit=10):
        options = {"offset": offset, "limit": limit}
        return self._request("GET", "/spaces", params=options)

    # --- members ---
    def getMember(self, spaceId: str, objectId: str):
        return self._request("GET", f"/spaces/{spaceId}/members/{objectId}")

    def getMembers(self, spaceId: str, offset: int, limit: int):
        options = {"offset": offset, "limit": limit}
        return self._request("GET", f"/spaces/{spaceId}/members", params=options)

    # def updateMember(self, spaceId: str, objectId: str, data: dict):
    #     return self._request(
    #         "PATCH", f"/spaces/{spaceId}/members/{objectId}", data=data
    #     )
    #     # NOTE: Not yet: https://github.com/anyproto/anytype-raycast/blob/ff6277ff34d1599e272d0fac443d3eb0b47304fa/src/components/ObjectActions.tsx#L203

    # --- types ---
    def getType(self, spaceId: str, typeId: str):
        return self._request("GET", f"/spaces/{spaceId}/types/{typeId}")

    def getTypes(self, spaceId: str, offset: int, limit: int):
        options = {"offset": offset, "limit": limit}
        return self._request("GET", f"/spaces/{spaceId}/types", params=options)

    # --- templates ---
    def getTemplate(self, spaceId: str, typeId: str, templateId: str):
        return self._request("GET", f"/spaces/{spaceId}/types/{typeId}/templates/{templateId}")

    def getTemplates(self, spaceId: str, typeId: str, offset: int, limit: int):
        options = {"offset": offset, "limit": limit}
        return self._request("GET", f"/spaces/{spaceId}/types/{typeId}/templates", params=options)


T = TypeVar("T", bound="APIWrapper")


class APIWrapper:
    _apiEndpoints: apiEndpoints | None = None

    @classmethod
    def _from_api(cls: Type[T], api: apiEndpoints, data: dict) -> T:
        instance = cls()
        instance._apiEndpoints = api
        instance._add_attrs_from_dict(data)
        return instance

    def _add_attrs_from_dict(self, data: dict) -> None:
        for key, value in data.items():
            self.__dict__[key] = value
