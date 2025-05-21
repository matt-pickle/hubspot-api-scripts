from typing import TypedDict, NotRequired, Literal, Any
import requests
import time

class Record(TypedDict):
    id: str
    properties: dict[str, Any]

class Response(TypedDict):
    results: list[Record]
    paging: NotRequired[dict[Literal["next"], dict[Literal["after"], str]]]

class UpdateInput(TypedDict):
    id: str
    properties: dict[str, Any]

def batch_update_records(
    record_type: str,
    inputs: list[UpdateInput],
    PRIVATE_APP_KEY: str
) -> list[Record]:
    url = f"https://api.hubapi.com/crm/v3/objects/{record_type}/batch/update"
    headers = { "Authorization": f"Bearer {PRIVATE_APP_KEY}", "Content-Type": "application/json"}
    records: list[Record] = []

    for i in range(0, len(inputs), 100):
        batch = inputs[i:i+100]
        data = { "inputs": batch }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            json_response: Response = response.json()
            print(f"Updated {record_type}: {len(json_response['results'])}")
            records.extend(json_response["results"])
        except requests.exceptions.RequestException as e:
            print(f"Error updating {record_type}: {e}")

        time.sleep(0.25)
    
    print(f"Total {record_type} updated: {len(records)}")
    return records