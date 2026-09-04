import json
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "NikhilBhatt-dev"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = Path("data/contributions.json")


def contribution_count(cell, soup):
    cell_id = cell.get("id")
    if cell_id:
        tip = soup.find("tool-tip", attrs={"for": cell_id})
        if tip:
            text = tip.get_text(" ", strip=True)
            match = re.search(r"([\d,]+)\s+contribution", text)
            if match:
                return int(match.group(1).replace(",", ""))

    text = cell.get_text(" ", strip=True)
    match = re.search(r"([\d,]+)\s+contribution", text)
    if match:
        return int(match.group(1).replace(",", ""))

    text = cell.get("data-tooltip-text", "")
    match = re.search(r"([\d,]+)\s+contribution", text)
    return int(match.group(1).replace(",", "")) if match else 0


def main():
    response = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0 GitHub-Contribution-Renderer",
            "Referer": f"https://github.com/{USERNAME}",
            "X-Requested-With": "XMLHttpRequest",
        },
        timeout=30,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    cells = soup.select("td.ContributionCalendar-day[data-date]")
    if not cells:
        raise RuntimeError("No contribution calendar cells found; GitHub markup may have changed.")

    days = []
    for cell in cells:
        date = cell.get("data-date")
        level = cell.get("data-level")
        if not date or level is None:
            continue
        days.append({
            "date": date,
            "level": int(level),
            "count": contribution_count(cell, soup),
        })

    days.sort(key=lambda item: item["date"])
    total = sum(item["count"] for item in days)

    payload = {
        "username": USERNAME,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total": total,
        "days": days,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved {len(days)} days and {total} contributions to {OUT}")


if __name__ == "__main__":
    main()
