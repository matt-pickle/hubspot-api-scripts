from functions.get_private_app_key import get_private_app_key
from functions.search_records import Record, SearchBody, search_records
from functions.batch_delete_records import batch_delete_records

PRIVATE_APP_KEY: str = get_private_app_key()

search_body: SearchBody = {
    "filterGroups": [
        {
            "filters": [
                {
                    "propertyName": "hs_note_body",
                    "operator": "NOT_CONTAINS_TOKEN",
                    "value": "Salesforce Migration files for record"
                }
            ]
        }
    ],
    "properties": ["hs_note_body"],
    "limit": 100,
    "after": 0
}
notes: list[Record] = search_records("notes", search_body, PRIVATE_APP_KEY)

notes_to_delete: list[Record] = []
for note in notes:
   if note["properties"]["hs_note_body"] is None or "Salesforce Migration files for record" not in note["properties"]["hs_note_body"]:
      notes_to_delete.append(note)

note_ids: list[str] = [note["id"] for note in notes_to_delete]

batch_delete_records("notes", note_ids, PRIVATE_APP_KEY)