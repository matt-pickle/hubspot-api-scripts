from dotenv import load_dotenv
import os
from functions.list_records import list_records
from functions.batch_delete_records import batch_delete_records

load_dotenv()
PRIVATE_APP_KEY = os.getenv("PRIVATE_APP_KEY")

all_notes = list_records("notes", ["hs_note_body"], PRIVATE_APP_KEY)

notes_to_delete = []
for note in all_notes:
   if note["properties"]["hs_note_body"] is None or "Salesforce Migration files for record" not in note["properties"]["hs_note_body"]:
      notes_to_delete.append(note)

note_ids = [note["id"] for note in notes_to_delete]

batch_delete_records("notes", note_ids, PRIVATE_APP_KEY)