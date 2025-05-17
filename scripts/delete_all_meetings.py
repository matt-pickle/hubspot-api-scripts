from utils.get_private_app_key import get_private_app_key
from requests.list_records import Record
from requests.list_records import list_records
from requests.batch_delete_records import batch_delete_records

PRIVATE_APP_KEY: str = get_private_app_key()

meetings_to_delete: list[Record] = list_records("meetings", [], PRIVATE_APP_KEY)

meeting_ids: list[str] = [meeting["id"] for meeting in meetings_to_delete]

batch_delete_records("meetings", meeting_ids, PRIVATE_APP_KEY)