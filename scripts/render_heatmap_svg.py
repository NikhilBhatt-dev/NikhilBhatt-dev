import json
from pathlib import Path
from datetime import datetime

W, H = 760, 250
CELL, GAP = 10, 3
LEFT, TOP = 44, 42
COLS = 53
ROWS = 7

LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def main():
    data = json.loads(Path("data/contributions.json").read_text(encoding="utf-8"))
    days = data["days"][-371:]
    total = data.get("total", sum(x["count"] for x in days))

    # Arrange newest year-ish window into 53 columns x 7 rows.
    by_date = {x["date"]: x for x in days}
    dates = [datetime.strptime(x["date"], "%Y-%m-%d").date() for x in days]
    start = dates[0] if dates else datetime.now().date()
    # Align the first column to Sunday.
    from datetime import timedelta
    start -= timedelta(days=(start.weekday() + 1) % 7)

    cells = []
    for i in range(COLS * ROWS):
        d = start + timedelta(days=i)
        item = by_date.get(d.isoformat(), {"level": 0, "count": 0})
        col, row = divmod(i, ROWS)
        x = LEFT + col * (CELL + GAP)
        y = TOP + row * (CELL + GAP)
        delay = 0.01 + col * 0.035 + row * 0.012
        color = LEVELS[min(4, max(0, int(item["level"]))) ]
        cells.append(f'''<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{color}" opacity="1"><animate attributeName="opacity" values="0;0;1" keyTimes="0;0.25;1" begin="{delay:.3f}s" dur="0.55s" fill="freeze"/><animateTransform attributeName="transform" type="scale" additive="sum" values="1 1;1.18 1.18;1 1" keyTimes="0;0.55;1" begin="{delay:.3f}s" dur="0.55s" fill="freeze"/></rect>''')

    weekdays = [("Mon",1),("Wed",3),("Fri",5)]
    labels = ''.join(f'<text x="10" y="{TOP+r*(CELL+GAP)+8}" fill="#8b949e" font-size="10">{name}</text>' for name,r in weekdays)
    month_labels = []
    last_month = None
    for c in range(COLS):
        idx = c * ROWS
        d = start + timedelta(days=idx)
        if d.month != last_month:
            month_labels.append(f'<text x="{LEFT+c*(CELL+GAP)}" y="25" fill="#8b949e" font-size="10">{d.strftime("%b")}</text>')
            last_month = d.month

    stars = []
    for i in range(0, COLS*ROWS, 31):
        col,row=divmod(i,ROWS); x=LEFT+col*(CELL+GAP)+CELL/2; y=TOP+row*(CELL+GAP)+CELL/2
        stars.append(f'<circle cx="{x}" cy="{y}" r="2" fill="#7ee787"><animate attributeName="opacity" values="0.2;1;0.2" keyTimes="0;0.08;1" begin="{0.5+(i%7)*0.7:.1f}s" dur="7s" repeatCount="indefinite"/></circle>')

    beam_x = LEFT-4
    beam_w = 16
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><clipPath id="grid"><rect x="{LEFT}" y="{TOP}" width="{COLS*(CELL+GAP)-GAP}" height="{ROWS*(CELL+GAP)-GAP}" rx="4"/></clipPath></defs>
<rect width="100%" height="100%" rx="14" fill="#0d1117" stroke="#30363d"/>
<circle cx="18" cy="15" r="4" fill="#ff5f56"/><circle cx="32" cy="15" r="4" fill="#ffbd2e"/><circle cx="46" cy="15" r="4" fill="#27c93f"/>
<text x="64" y="19" fill="#8b949e" font-family="monospace" font-size="10">contributions.sh</text>
{labels}{''.join(month_labels)}
<g font-family="monospace">{''.join(cells)}</g>
<g clip-path="url(#grid)"><rect x="{beam_x}" y="{TOP-4}" width="{beam_w}" height="{ROWS*(CELL+GAP)+8}" fill="#39d353" opacity="0.10"><animate attributeName="x" from="{beam_x}" to="{LEFT+COLS*(CELL+GAP)}" dur="9s" repeatCount="indefinite"/></rect></g>
{''.join(stars)}
<text x="44" y="218" fill="#8b949e" font-family="monospace" font-size="11">total contributions:</text>
<text x="190" y="218" fill="#39d353" font-family="monospace" font-size="11">{esc(total)}</text>
<text x="235" y="218" fill="#39d353" font-family="monospace" font-size="11">▌<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></text>
<text x="520" y="218" fill="#8b949e" font-family="monospace" font-size="10">less</text>
{''.join(f'<rect x="{555+i*16}" y="210" width="11" height="11" rx="2" fill="{c}"/>' for i,c in enumerate(LEVELS))}
<text x="640" y="218" fill="#8b949e" font-family="monospace" font-size="10">more</text>
</svg>'''
    Path("assets").mkdir(exist_ok=True)
    Path("assets/heatmap.svg").write_text(svg, encoding="utf-8")

if __name__ == "__main__": main()
