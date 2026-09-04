import json
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "NikhilBhatt-dev"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = Path("data/contributions.json")


def extract_count(cell, soup):
    # GitHub currently exposes the count in the cell's tooltip target.
    target_id = cell.get("aria-describedby")
    if target_id:
        tip = soup.find(id=target_id)
        if tip:
            text = tip.get_text(" ", strip=True)
            m = re.search(r"([\d,]+) contribution", text)
            if m:
                return int(m.group(1).replace(",", ""))

    # Fallback: look at common tooltip attributes/content.
    for node in cell.find_all(attrs={"data-tooltip-text": True}):
        text = node.get("data-tooltip-text", "")
        m = re.search(r"([\d,]+) contribution", text)
        if m:
            return int(m.group(1).replace(",", ""))

    text = cell.get("data-tooltip-text", "")
    m = re.search(r"([\d,]+) contribution", text)
    return int(m.group(1).replace(",", "")) if m else 0


def main():
    r = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0 GitHub-Contribution-Renderer"},
        timeout=30,
    )
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        # GitHub has also used rect elements in some calendar variants.
        cells = soup.select("rect.ContributionCalendar-day")

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
            "count": extract_count(cell, soup),
        })

    days.sort(key=lambda x: x["date"])
    total = sum(d["count"] for d in days)

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
