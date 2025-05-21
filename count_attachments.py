from functions.get_private_app_key import get_private_app_key
from functions.list_records import Record, list_records

PRIVATE_APP_KEY: str = get_private_app_key()

notes: list[Record] = list_records("notes", ["hs_note_body","hs_attachment_ids"], PRIVATE_APP_KEY)

attachment_ids: list[str] = []
for note in notes:
    if "Salesforce Migration files for record" in note["properties"]["hs_note_body"]:
        if note["properties"]["hs_attachment_ids"] is None:
            print("NO FILE IDS FOR NOTE: " + note["id"])
        else:
            these_attachment_ids: list[str] = note["properties"]["hs_attachment_ids"].split(";")
            attachment_ids.extend(these_attachment_ids)

print(f"Total attachments: {len(attachment_ids)}")