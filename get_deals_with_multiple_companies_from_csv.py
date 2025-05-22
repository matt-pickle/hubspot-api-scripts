from functions.get_private_app_key import get_private_app_key
from functions.parse_csv import parse_csv
from functions.batch_read_associations import Association, batch_read_associations
from functions.write_to_csv import write_to_csv

PRIVATE_APP_KEY: str = get_private_app_key()

deals: list[dict] = parse_csv("input/rms-opportunities.csv")

all_deal_ids: list[str] = [deal["Record ID"] for deal in deals]

associations: list[Association] = batch_read_associations("deals", "companies", all_deal_ids, PRIVATE_APP_KEY)

deal_ids: list[dict] = []

for assoc in associations:
    if len(assoc["to"]) > 1:
        deal_id: dict = { "id": assoc["from"]["id"] }
        deal_ids.append(deal_id)

write_to_csv("rms_deals_with_multiple_companies", ["id"], deal_ids)