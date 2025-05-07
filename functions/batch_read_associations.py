import requests
import time

def batch_read_associations(fromRecordType, toRecordType, ids, PRIVATE_APP_KEY):
   url = f"https://api.hubapi.com/crm/v4/associations/{fromRecordType}/{toRecordType}/batch/read"
   headers = { "Authorization": f"Bearer {PRIVATE_APP_KEY}", "Content-Type": "application/json"}
   results = []

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
         json_response = response.json()
         results.extend(json_response["results"])
         print(f"Retrieved {fromRecordType}<>{toRecordType} associations: {len(json_response["results"])}")
      except requests.exceptions.RequestException as e:
         print(f"Error retrieving {fromRecordType}<>{toRecordType} associations: {e}")

      time.sleep(0.25)

   return results