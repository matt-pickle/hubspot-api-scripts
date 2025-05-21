import os
import csv
from datetime import datetime

def write_to_csv(title: str, fieldnames: list[str], data: list[dict]) -> None:
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  csv_filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", f"{title}_{timestamp}.csv")
  if data and len(data) > 0:
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
      writer.writeheader()
      writer.writerows(data)
    print(f"Exported {len(data)} {title} to {csv_filename}")