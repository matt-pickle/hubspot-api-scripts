from typing import TypedDict, NotRequired, Literal, Any
import requests
import time

class Record(TypedDict):
    id: str
    properties: dict[str, Any]

class Response(TypedDict):
    results: list[Record]
    paging: NotRequired[dict[Literal["next"], dict[Literal["after"], str]]]

def list_records(
    recordType: str,
    propertyNames: list[str],
    PRIVATE_APP_KEY: str,
    after: str = "",
    records: list[Record] = []
) -> list[Record]:
    if records is None:
        records = []
    url = f"https://api.hubapi.com/crm/v3/objects/{recordType}?limit=100"
    if len(propertyNames) > 0:
        url += f"&properties={','.join(propertyNames)}"
    if after:
        url += f"&after={after}"
    headers = { "Authorization": f"Bearer {PRIVATE_APP_KEY}", "Content-Type": "application/json"}
        
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_response: Response = response.json()
        print(f"Retrieved {recordType}: {len(json_response['results'])}")
        records.extend(json_response["results"])
        paging = json_response.get("paging")
        if paging:
            next = paging.get("next")
            if next:
                new_after = next.get("after")
                if new_after:
                    time.sleep(0.25)
                    return list_records(recordType, propertyNames, PRIVATE_APP_KEY, new_after, records)
    except requests.exceptions.RequestException as e:
        print(f"Error getting {recordType}: {e}")

    print(f"Total {recordType} retrieved: {len(records)}")
    return records