from functions.get_private_app_key import get_private_app_key
from functions.search_records import Record, SearchBody, search_records
from functions.batch_read_associations import Association, batch_read_associations
from functions.batch_delete_records import batch_delete_records

PRIVATE_APP_KEY: str = get_private_app_key()

search_body: SearchBody = {
    "filterGroups": [
        {
            "filters": [
                {
                    "propertyName": "rms_salesforce_id",
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

associations: list[Association] = batch_read_associations("deals", "line_items", deal_ids, PRIVATE_APP_KEY)

line_item_ids: list[str] = []

for assoc in associations:
    to: list[dict] = [ { "id": to["toObjectId"] } for to in assoc["to"]]
    line_item_ids.extend([item["id"] for item in to])

print(f"Total Line Items: {len(line_item_ids)}")

batch_delete_records("line_items", line_item_ids, PRIVATE_APP_KEY)