from typing import TypedDict, Literal
import requests

AssociationInput = TypedDict(
    "AssociationInput",
    {
        "from": dict[Literal["id"], str],
        "to": list[dict[Literal["id"], str]]
    },
)

def batch_unassociate_records(
    fromRecordType: str,
    toRecordType: str,
    inputs: list[AssociationInput],
    PRIVATE_APP_KEY: str
) -> None:
    url = f"https://api.hubapi.com/crm/v4/associations/{fromRecordType}/{toRecordType}/batch/archive"
    headers = { "Authorization": f"Bearer {PRIVATE_APP_KEY}", "Content-Type": "application/json"}

    for i in range(0, len(inputs), 500):
        batch = inputs[i:i+500]
        data = { "inputs": batch }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"Unassociated {fromRecordType} from {toRecordType}: {len(batch)}")
        except requests.exceptions.RequestException as e:
            print(f"Error unassociating {fromRecordType} from {toRecordType}: {e}")