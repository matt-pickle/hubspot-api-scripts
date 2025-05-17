from utils.get_private_app_key import get_private_app_key
from requests.list_records import Record
from requests.list_records import list_records
from requests.batch_read_associations import Association
from requests.batch_read_associations import batch_read_associations
from requests.batch_unassociate_records import AssociationInput
from requests.batch_unassociate_records import batch_unassociate_records

PRIVATE_APP_KEY: str = get_private_app_key()

contacts: list[Record] = list_records("contacts", [], PRIVATE_APP_KEY)

contact_ids: list[str] = [contact["id"] for contact in contacts]

associations: list[Association] = batch_read_associations("contacts", "deals", contact_ids, PRIVATE_APP_KEY)

inputs: list[AssociationInput] = []
for assoc in associations:
    to: list[dict] = [ { "id": to["toObjectId"] } for to in assoc["to"]]
    input: AssociationInput = { "from": assoc["from"], "to": to }
    inputs.append(input)

batch_unassociate_records("contacts", "deals", inputs, PRIVATE_APP_KEY)