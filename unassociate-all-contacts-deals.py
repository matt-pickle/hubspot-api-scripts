from dotenv import load_dotenv
import os
from functions.list_records import list_records
from functions.batch_read_associations import batch_read_associations
from functions.batch_unassociate_records import batch_unassociate_records

load_dotenv()
PRIVATE_APP_KEY = os.getenv("PRIVATE_APP_KEY")

contacts = list_records("contacts", [], PRIVATE_APP_KEY)

contact_ids = [contact["id"] for contact in contacts]

associations = batch_read_associations("contacts", "deals", contact_ids, PRIVATE_APP_KEY)

inputs = []
for assoc in associations:
   input = {}
   input["from"] = assoc["from"]
   to = []
   for to_assoc in assoc["to"]:
      to.append({ "id": to_assoc["toObjectId"] })
   input["to"] = to
   inputs.append(input)

batch_unassociate_records("contacts", "deals", inputs, PRIVATE_APP_KEY)