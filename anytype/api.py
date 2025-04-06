import requests

import requests
from urllib.parse import urlencode

API_CONFIG = {
    "apiUrl": "http://localhost:31009/v1",
    "apiAppName": "PythonClient",
}


class apiEndpoints:
    def __init__(self, headers: dict = {}):
        self.api_url = API_CONFIG["apiUrl"].rstrip("/")
        self.app_name = API_CONFIG["apiAppName"]
        self.headers = headers

    def _request(self, method, path, params=None, data=None):
        url = f"{self.api_url}{path}"
        if params:
            url += "?" + urlencode(params)
        response = requests.request(
            method, url, headers=self.headers, json=data
        )
        response.raise_for_status()
        return response.json()

    # --- auth ---
    def displayCode(self):
        return self._request(
            "POST", "/auth/display_code", params={"app_name": self.app_name}
        )

    def getToken(self, challengeId: str, code: str):
        return self._request(
            "POST",
            "/auth/token",
            params={"challenge_id": challengeId, "code": code},
        )

    # --- export ---
    def getExport(self, spaceId: str, objectId: str, format: str):
        return self._request(
            "GET", f"/spaces/{spaceId}/objects/{objectId}/{format}"
        )
        # TODO:

    # --- lists ---
    def getListViews(self, spaceId: str, listId: str, options: dict):
        return self._request(
            "GET", f"/spaces/{spaceId}/lists/{listId}/views", params=options
        )
        # TODO:

    def getObjectsInList(
        self, spaceId: str, listId: str, viewId: str, options: dict
    ):
        return self._request(
            "GET",
            f"/spaces/{spaceId}/lists/{listId}/{viewId}/objects",
            params=options,
        )
        # TODO:

    def addObjectsToList(self, spaceId: str, listId: str, data: dict):
        return self._request(
            "POST", f"/spaces/{spaceId}/lists/{listId}/objects", data=data
        )
        # TODO:

    def removeObjectsFromList(self, spaceId: str, listId: str, objectId: str):
        return self._request(
            "DELETE", f"/spaces/{spaceId}/lists/{listId}/objects/{objectId}"
        )
        # TODO:

    # --- objects ---
    def createObject(self, spaceId: str, data: dict):
        return self._request("POST", f"/spaces/{spaceId}/objects", data=data)

    def deleteObject(self, spaceId: str, objectId: str):
        return self._request("DELETE", f"/spaces/{spaceId}/objects/{objectId}")
        # TODO:

    def getObject(self, spaceId: str, objectId: str):
        return self._request("GET", f"/spaces/{spaceId}/objects/{objectId}")
        # TODO:

    def getObjects(self, spaceId: str, offset=0, limit=10):
        options = {"offset": offset, "limit": limit}
        return self._request(
            "GET", f"/spaces/{spaceId}/objects", params=options
        )
        # TODO:

    # --- search ---
    def globalSearch(self, query: str = "", offset=0, limit=10):
        options = {"offset": offset, "limit": limit}
        payload = {"query": query}
        return self._request("POST", "/search", params=options, data=payload)

    def search(
        self, spaceId: str, query: str, offset: int = 0, limit: int = 10
    ):
        options = {"offset": offset, "limit": limit}
        payload = {"query": query}
        return self._request(
            "POST", f"/spaces/{spaceId}/search", params=options, data=payload
        )

    # --- spaces ---
    def createSpace(self, name):
        data = {"name": name}
        return self._request("POST", "/spaces", data=data)

    def getSpace(self, spaceId: str):
        return self._request("GET", f"/spaces/{spaceId}")
        # TODO:

    def getSpaces(self, offset=0, limit=10):
        options = {"offset": offset, "limit": limit}
        return self._request("GET", "/spaces", params=options)
        # TODO:

    # --- members ---
    def getMember(self, spaceId: str, objectId: str):
        return self._request("GET", f"/spaces/{spaceId}/members/{objectId}")
        # TODO:

    def getMembers(self, spaceId: str, offset: int, limit: int):
        options = {"offset": offset, "limit": limit}
        return self._request(
            "GET", f"/spaces/{spaceId}/members", params=options
        )

    def updateMember(self, spaceId: str, objectId: str, data: dict):
        return self._request(
            "PATCH", f"/spaces/{spaceId}/members/{objectId}", data=data
        )
        # TODO:

    # --- types ---
    def getType(self, spaceId: str, typeId: str):
        return self._request("GET", f"/spaces/{spaceId}/types/{typeId}")

    def getTypes(self, spaceId: str, offset: int, limit: int):
        options = {"offset": offset, "limit": limit}
        return self._request("GET", f"/spaces/{spaceId}/types", params=options)
        # TODO:

    # --- templates ---
    def getTemplate(self, spaceId: str, typeId: str, templateId: str):
        return self._request(
            "GET", f"/spaces/{spaceId}/types/{typeId}/templates/{templateId}"
        )
        # TODO:

    def getTemplates(self, spaceId: str, typeId: str, options: dict):
        return self._request(
            "GET", f"/spaces/{spaceId}/types/{typeId}/templates", params=options
        )
        # TODO:
