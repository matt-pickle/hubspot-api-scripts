from typing import TypedDict, NotRequired, Literal, Any
import requests
import time

class Record(TypedDict):
    id: str
    properties: dict[str, Any]

class Filter(TypedDict):
    propertyName: str
    operator: Literal["IN"] | Literal["NOT_HAS_PROPERTY"] | Literal["LT"] | Literal["EQ"] | Literal["GT"] | Literal["NOT_IN"] | Literal["GTE"] | Literal["CONTAINS_TOKEN"] | Literal["HAS_PROPERTY"] | Literal["LTE"] | Literal["NOT_CONTAINS_TOKEN"] | Literal["BETWEEN"] | Literal["NEQ"]
    values: NotRequired[list[str]]
    value: NotRequired[str]

class SearchBody(TypedDict):
    filterGroups: list[dict[Literal["filters"], list[Filter]]]
    properties: list[str]
    limit: int
    after: NotRequired[str | int]
    sorts: NotRequired[list[dict[str, str]]]

class Response(TypedDict):
    results: list[Record]
    total: int
    paging: NotRequired[dict[Literal["next"], dict[Literal["after"], str]]]

def search_records(
    record_type: str,
    search_body: SearchBody,
    PRIVATE_APP_KEY: str,
    records: list[Record] | None = None
) -> list[Record]:
    if records is None:
        records = []
    url = f"https://api.hubapi.com/crm/v3/objects/{record_type}/search"
    headers = { "Authorization": f"Bearer {PRIVATE_APP_KEY}", "Content-Type": "application/json"}
        
    try:
        response = requests.post(url, headers=headers, json=search_body)
        response.raise_for_status()
        json_response: Response = response.json()
        print(f"Retrieved {record_type}: {len(json_response['results'])}")
        records.extend(json_response["results"])
        paging = json_response.get("paging")
        if paging:
            next = paging.get("next")
            if next:
                new_after = next.get("after")
                if new_after:
                    search_body["after"] = new_after
                    time.sleep(0.25)
                    return search_records(record_type, search_body, PRIVATE_APP_KEY, records)
    except requests.exceptions.RequestException as e:
        print(f"Error getting {record_type}: {e}")

    print(f"Total {record_type} retrieved: {len(records)}")
    return records