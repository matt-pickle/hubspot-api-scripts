from functions.get_private_app_key import get_private_app_key
from functions.search_folders import search_folders
from functions.search_files import search_files
from functions.write_to_csv import write_to_csv

PRIVATE_APP_KEY: str = get_private_app_key()

count: int = 0
files: list[dict] = []
folders: list[dict] = []
has_more: bool = True
starting_id: int = 0

while has_more is True:
    folders_batch: list[dict] = search_folders(PRIVATE_APP_KEY, "189897552745", starting_id)
    folders.extend(folders_batch)
    print(f"Fetched {len(folders_batch)} folders")
    print(f"Total folders so far: {len(folders)}")
    if len(folders_batch) < 9900:
        has_more = False
        break
    starting_id = int(folders_batch[-1]["id"]) + 1
    print(f"Next starting ID: {starting_id}")

for folder in folders:
    these_files: list[dict] = search_files(PRIVATE_APP_KEY, folder["id"])
    files.extend(these_files)
    count += len(these_files)

print(f"Total files in all folders: {count}")

files_to_write: list[dict] = [{ "id": file["id"], "name": file["name"], "path": file["path"], "createdAt": file["createdAt"] } for file in files]
write_to_csv("opp_files.csv", ["id", "name", "path", "createdAt"], files_to_write)