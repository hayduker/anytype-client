API_CONFIG = {
    "apiUrl": "http://localhost:31009/v1",
    "apiAppName": "PythonClient",
}

# getListViews: (spaceId: string, listId: string, options: { offset: number; limit: number }) => ({
#   url: `${apiUrl}/spaces/${spaceId}/lists/${listId}/views${encodeQueryParams(options)}`,
#   method: "GET",
# }),
# getObjectsInList: (spaceId: string, listId: string, viewId: string, options: { offset: number; limit: number }) => ({
#   url: `${apiUrl}/spaces/${spaceId}/lists/${listId}/${viewId}/objects${encodeQueryParams(options)}`,
#   method: "GET",
# }),
# addObjectsToList: (spaceId: string, listId: string) => ({
#   url: `${apiUrl}/spaces/${spaceId}/lists/${listId}/objects`,
#   method: "POST",
# }),
# removeObjectsFromList: (spaceId: string, listId: string, objectId: string) => ({
#   url: `${apiUrl}/spaces/${spaceId}/lists/${listId}/objects/${objectId}`,
#   method: "DELETE",
# }),

END_POINTS = {
    "auth": "{}/auth/token".format(API_CONFIG["apiUrl"]),
    "createObject": "{}/spaces/{}/objects".format(API_CONFIG["apiUrl"], "{}"),
    "createSpace": "{}/spaces".format(API_CONFIG["apiUrl"]),
    "deleteSpace": "{}/spaces/{}".format(API_CONFIG["apiUrl"], "{}"),
    "deleteObject": "{}/spaces/{}/objects/{}".format(
        API_CONFIG["apiUrl"], "{}", "{}"
    ),
    "displayCode": "{}/auth/display_code".format(API_CONFIG["apiUrl"]),
    "getExport": "{}/spaces/{}/objects/{}/{}".format(
        API_CONFIG["apiUrl"], "{}", "{}", "{}"
    ),
    "getMembers": "{}/spaces/{}/members".format(
        API_CONFIG["apiUrl"],
        "{}",
    ),
    "getObject": "{}/spaces/{}/objects/{}".format(
        API_CONFIG["apiUrl"], "{}", "{}"
    ),
    "getObjects": "{}/spaces/{}/objects".format(API_CONFIG["apiUrl"], "{}"),
    "getSpaces": "{}/spaces".format(API_CONFIG["apiUrl"]),
    "getTemplates": "{}/spaces/{}/types/{}/templates".format(
        API_CONFIG["apiUrl"],
        "{}",
        "{}",
    ),
    "getToken": "{}/auth/token".format(
        API_CONFIG["apiUrl"],
    ),
    "getTypes": "{}/spaces/{}/types".format(API_CONFIG["apiUrl"], "{}"),
    "globalSearch": "{}/search".format(API_CONFIG["apiUrl"]),
    "search": "{}/spaces/{}/search".format(API_CONFIG["apiUrl"], "{}"),
}
