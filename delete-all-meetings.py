from dotenv import load_dotenv
import os
from functions.list_records import list_records
from functions.batch_delete_records import batch_delete_records

load_dotenv()
PRIVATE_APP_KEY = os.getenv("PRIVATE_APP_KEY")

meetings_to_delete = list_records("meetings", [], PRIVATE_APP_KEY)

meeting_ids = [meeting["id"] for meeting in meetings_to_delete]

batch_delete_records("meetings", meeting_ids, PRIVATE_APP_KEY)