import requests
import time

def batch_delete_records(recordType: str, ids: list[str], PRIVATE_APP_KEY: str) -> None:
    url = f"https://api.hubapi.com/crm/v3/objects/{recordType}/batch/archive"
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
            print(f"Deleted {recordType}: {len(batch)}")
        except requests.exceptions.RequestException as e:
            print(f"Error deleting {recordType}: {e}")

        time.sleep(0.25)