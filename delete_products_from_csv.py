from functions.get_private_app_key import get_private_app_key
from functions.parse_csv import parse_csv
from functions.batch_delete_records import batch_delete_records

PRIVATE_APP_KEY: str = get_private_app_key()

products_to_delete: list[dict] = parse_csv("input/RMS Products - to delete.csv")

product_ids: list[str] = [product["Record ID"] for product in products_to_delete]

batch_delete_records("products", product_ids, PRIVATE_APP_KEY)