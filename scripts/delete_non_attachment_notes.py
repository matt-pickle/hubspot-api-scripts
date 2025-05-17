from utils.get_private_app_key import get_private_app_key
from requests.list_records import Record
from requests.list_records import list_records
from requests.batch_delete_records import batch_delete_records

PRIVATE_APP_KEY: str = get_private_app_key()

all_notes: list[Record] = list_records("notes", ["hs_note_body"], PRIVATE_APP_KEY)

notes_to_delete: list[Record] = []
for note in all_notes:
   if note["properties"]["hs_note_body"] is None or "Salesforce Migration files for record" not in note["properties"]["hs_note_body"]:
      notes_to_delete.append(note)

note_ids: list[str] = [note["id"] for note in notes_to_delete]

batch_delete_records("notes", note_ids, PRIVATE_APP_KEY)