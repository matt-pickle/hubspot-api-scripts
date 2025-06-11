import requests
import time

def batch_delete_records(record_type: str, ids: list[str], PRIVATE_APP_KEY: str) -> None:
    url = f"https://api.hubapi.com/crm/v3/objects/{record_type}/batch/archive"
    headers = { "Authorization": f"Bearer {PRIVATE_APP_KEY}", "Content-Type": "application/json"}

    for i in range(0, len(ids), 100):
        batch = ids[i:i+100]
        inputs = []
        for id in batch:
            input = { "id": id }
            inputs.append(input)
        data = { "inputs": inputs }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"Deleted {record_type}: {len(batch)}")
        except requests.exceptions.RequestException as e:
            print(f"Error deleting {record_type}: {e}")

        time.sleep(0.25)