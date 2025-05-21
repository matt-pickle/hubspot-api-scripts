from typing import TypedDict, NotRequired, Literal, Any
import requests
import time

class Response(TypedDict):
    results: list[dict[str, Any]]
    paging: NotRequired[dict[Literal["next"], dict[Literal["after"], str]]]

def search_files(
    PRIVATE_APP_KEY: str,
    parent_folder_ids: str = "",
    after: str = "",
    records: list[dict[str, Any]] | None = None
) -> list[dict[str, Any]]:
    if records is None:
        records = []
    url = f"https://api.hubapi.com/files/v3/files/search?limit=100"
    if parent_folder_ids:
        url += f"&parentFolderIds={parent_folder_ids}"
    if after:
        url += f"&after={after}"
    headers = { "Authorization": f"Bearer {PRIVATE_APP_KEY}", "Content-Type": "application/json"}
        
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_response: Response = response.json()
        print(f"Retrieved files: {len(json_response['results'])}")
        records.extend(json_response["results"])
        paging = json_response.get("paging")
        if paging:
            next = paging.get("next")
            if next:
                new_after = next.get("after")
                if new_after:
                    time.sleep(0.25)
                    return search_files(PRIVATE_APP_KEY, parent_folder_ids, new_after, records)
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}. Retrying...")
        time.sleep(1)
        return search_files(PRIVATE_APP_KEY, parent_folder_ids, after, records)
    except requests.exceptions.RequestException as e:
        print(f"Error getting files: {e}")

    print(f"Total files retrieved: {len(records)}")
    return records