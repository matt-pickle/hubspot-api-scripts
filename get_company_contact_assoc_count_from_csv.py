from functions.get_private_app_key import get_private_app_key
from functions.parse_csv import parse_csv
from functions.batch_read_associations import Association, batch_read_associations

PRIVATE_APP_KEY: str = get_private_app_key()

companies: list[dict] = parse_csv("input/rms-accounts.csv")

company_ids: list[str] = [company["Record ID"] for company in companies]

associations: list[Association] = batch_read_associations("companies", "contacts", company_ids, PRIVATE_APP_KEY)

contact_ids: list[str] = []

for assoc in associations:
    to: list[dict] = [ { "id": to["toObjectId"] } for to in assoc["to"]]
    contact_ids.extend([item["id"] for item in to])

print(f"Total associations: {len(contact_ids)}")