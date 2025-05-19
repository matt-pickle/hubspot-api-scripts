from functions.get_private_app_key import get_private_app_key
from functions.search_records import Record, SearchBody, search_records
from functions.batch_read_associations import Association, batch_read_associations

PRIVATE_APP_KEY: str = get_private_app_key()

search_body: SearchBody = {
    "filterGroups": [
        {
            "filters": []
        }
    ],
    "properties": [],
    "limit": 100,
    "after": 0
}
quotes: list[Record] = search_records("quotes", search_body, PRIVATE_APP_KEY)

quote_ids: list[str] = [quote["id"] for quote in quotes]

associations: list[Association] = batch_read_associations("quotes", "line_items", quote_ids, PRIVATE_APP_KEY)

line_item_ids: list[str] = []

for assoc in associations:
    to: list[dict] = [ { "id": to["toObjectId"] } for to in assoc["to"]]
    line_item_ids.extend([item["id"] for item in to])

print(f"Total Line Items: {len(line_item_ids)}")