"""
Refresh data/online_share.csv from the official ONS source (series J4MC:
internet sales as a percentage of total retail sales, Great Britain).

    python fetch_ons.py

Writes every annual value ONS publishes, replacing the snapshot in data/.
"""
import csv
import io
import re
from pathlib import Path

import requests

URL = ("https://www.ons.gov.uk/generator?format=csv"
       "&uri=/businessindustryandtrade/retailindustry/timeseries/j4mc/drsi")
OUT = Path(__file__).parent / "data" / "online_share.csv"


def main():
    resp = requests.get(URL, timeout=30, headers={"User-Agent": "uk-high-street-turnaround"})
    resp.raise_for_status()
    rows = csv.reader(io.StringIO(resp.content.decode("utf-8-sig")))
    annual = [(int(r[0]), float(r[1])) for r in rows
              if len(r) >= 2 and re.fullmatch(r"\d{4}", r[0].strip()) and r[1].strip()]
    if not annual:
        raise SystemExit("No annual rows found: the ONS file format may have changed.")
    with OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "online_share_pct"])
        w.writerows(annual)
    print(f"Wrote {len(annual)} years ({annual[0][0]}–{annual[-1][0]}) to {OUT}")


if __name__ == "__main__":
    main()
