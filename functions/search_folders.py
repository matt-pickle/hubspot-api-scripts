from typing import TypedDict, NotRequired, Literal, Any
import requests
import time

class Response(TypedDict):
    results: list[dict[str, Any]]
    paging: NotRequired[dict[Literal["next"], dict[Literal["after"], str]]]

def search_folders(
    PRIVATE_APP_KEY: str,
    parent_folder_ids: str = "",
    starting_id: int | None = None,
    after: str | None = None,
    records: list[dict[str, Any]] | None = None,
    count: int = 1
) -> list[dict[str, Any]]:
    if records is None:
        records = []
    url = f"https://api.hubapi.com/files/v3/folders/search?limit=100&sort=id"
    if parent_folder_ids:
        url += f"&parentFolderIds={parent_folder_ids}"
    if after:
        url += f"&after={after}"
    if starting_id:
        url += f"&idGte={starting_id}"
    headers = { "Authorization": f"Bearer {PRIVATE_APP_KEY}", "Content-Type": "application/json"}
        
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_response: Response = response.json()
        print(f"Retrieved folders: {len(json_response['results'])}")
        records.extend(json_response["results"])
        paging = json_response.get("paging")
        if paging:
            next = paging.get("next")
            if next:
                new_after = next.get("after")
                if new_after and count < 99:
                    count += 1
                    time.sleep(0.25)
                    return search_folders(PRIVATE_APP_KEY, parent_folder_ids, starting_id, new_after, records, count)
    except requests.exceptions.RequestException as e:
        print(f"Error getting folders: {e}")

    print(f"Total folders retrieved: {len(records)}")
    return records