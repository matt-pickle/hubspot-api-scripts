import requests
import time

def list_records(recordType, properties, PRIVATE_APP_KEY, after=0, records=None):
   if records is None:
      records = []
   url = f"https://api.hubapi.com/crm/v3/objects/{recordType}?limit=100"
   if len(properties) > 0:
      url += f"&properties={properties.join(",")}"
   if after:
      url += f"&after={after}"
   headers = { "Authorization": f"Bearer {PRIVATE_APP_KEY}", "Content-Type": "application/json"}
    
   try:
      response = requests.get(url, headers=headers)
      response.raise_for_status()
      json_response = response.json()
      print(f"Retrieved {recordType}: {len(json_response["results"])}")
      records.extend(json_response["results"])
      if json_response["paging"]["next"]["after"]:
         time.sleep(0.25)
         new_after = json_response["paging"]["next"]["after"]
         return list_records(recordType, properties, PRIVATE_APP_KEY, new_after, records)
   except requests.exceptions.RequestException as e:
      print(f"Error getting {recordType}: {e}")

   print(f"Total {recordType} retrieved: {len(records)}")
   return records