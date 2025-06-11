from typing import TypedDict, NotRequired, Literal
import requests
import time

Association = TypedDict(
    "Association",
    {
        "from": dict[Literal["id"], str],
        "to": list[dict[Literal["toObjectId"], str]]
    }
)

class Response(TypedDict):
    results: list[Association]

def batch_read_associations(
    fromRecordType: str,
    toRecordType: str,
    ids: list[str],
    PRIVATE_APP_KEY: str
) -> list[Association]:
    url = f"https://api.hubapi.com/crm/v4/associations/{fromRecordType}/{toRecordType}/batch/read"
    headers = { "Authorization": f"Bearer {PRIVATE_APP_KEY}", "Content-Type": "application/json"}
    results: list[Association] = []

    for i in range(0, len(ids), 500):
        batch = ids[i:i+500]
        inputs = []
        for id in batch:
            input = { "id": id }
            inputs.append(input)
        data = { "inputs": inputs }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            json_response: Response = response.json()
            results.extend(json_response["results"])
            print(f"Retrieved {fromRecordType}<>{toRecordType} associations: {len(json_response['results'])}")
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving {fromRecordType}<>{toRecordType} associations: {e}")

        time.sleep(0.25)

    return results