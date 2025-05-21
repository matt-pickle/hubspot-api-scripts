from functions.get_private_app_key import get_private_app_key
from functions.parse_csv import parse_csv
from functions.batch_update_records import UpdateInput, batch_update_records

PRIVATE_APP_KEY: str = get_private_app_key()

quotes: list[dict] = parse_csv("input/quotes.csv")

updateInputs: list[UpdateInput] = [
    {
        "id": quote["hs_id"],
        "properties": {
            "rms_salesforce_id": quote["sf_id"]
        }
    }
    for quote in quotes
]
batch_update_records("quotes", updateInputs, PRIVATE_APP_KEY)

