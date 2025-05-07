import requests
import time

def batch_unassociate_records(fromRecordType, toRecordType, inputs, PRIVATE_APP_KEY):
   url = f"https://api.hubapi.com/crm/v4/associations/{fromRecordType}/{toRecordType}/batch/archive"
   headers = { "Authorization": f"Bearer {PRIVATE_APP_KEY}", "Content-Type": "application/json"}

   for i in range(0, len(inputs), 100):
      batch = inputs[i:i+100]
      data = { "inputs": batch }

      try:
         response = requests.post(url, headers=headers, json=data)
         response.raise_for_status()
         print(f"Unassociated {fromRecordType} from {toRecordType}: {len(batch)}")
      except requests.exceptions.RequestException as e:
         print(f"Error unassociating {fromRecordType} from {toRecordType}: {e}")

      time.sleep(0.25)