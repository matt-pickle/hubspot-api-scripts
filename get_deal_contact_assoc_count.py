from functions.get_private_app_key import get_private_app_key
from functions.search_records import Record, SearchBody, search_records
from functions.batch_read_associations import Association, batch_read_associations

PRIVATE_APP_KEY: str = get_private_app_key()

search_body: SearchBody = {
    "filterGroups": [
        {
            "filters": [
                {
                    "propertyName": "rms_salesforce_id_",
                    "operator": "HAS_PROPERTY"
                }
            ]
        }
    ],
    "properties": [],
    "limit": 100,
    "after": 0
}
deals: list[Record] = search_records("deals", search_body, PRIVATE_APP_KEY)

deal_ids: list[str] = [deal["id"] for deal in deals]

associations: list[Association] = batch_read_associations("deals", "contacts", deal_ids, PRIVATE_APP_KEY)

contact_ids: list[str] = []

for assoc in associations:
    to: list[dict] = [ { "id": to["toObjectId"] } for to in assoc["to"]]
    contact_ids.extend([item["id"] for item in to])

print(f"Total associations: {len(contact_ids)}")