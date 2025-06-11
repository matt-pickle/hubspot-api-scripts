from typing import TypedDict, Literal
import requests

class AssociationType(TypedDict):
    associationCategory: Literal["HUBSPOT_DEFINED", "USER_DEFINED"]
    associationTypeId: int

CreateAssocInput = TypedDict(
    "CreateAssocInput",
    {
        "types": list[AssociationType],
        "from": dict[Literal["id"], str],
        "to": dict[Literal["id"], str]
    }
)

def batch_create_associations(
    fromRecordType: str,
    toRecordType: str,
    inputs: list[CreateAssocInput],
    PRIVATE_APP_KEY: str
) -> list[dict]:
    url = f"https://api.hubapi.com/crm/v4/associations/{fromRecordType}/{toRecordType}/batch/create"
    headers = { "Authorization": f"Bearer {PRIVATE_APP_KEY}", "Content-Type": "application/json"}
    results: list[dict] = []

    for i in range(0, len(inputs), 500):
        batch = inputs[i:i+500]
        data = { "inputs": batch }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            json_response = response.json()
            results.extend(json_response["results"])
            print(f"Associated {fromRecordType} to {toRecordType}: {len(json_response['results'])}")
        except requests.exceptions.RequestException as e:
            print(f"Error associating {fromRecordType} to {toRecordType}: {e}")

    return results