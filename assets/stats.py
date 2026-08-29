# Renders the GitHub statistics panel from the REST API.
#
# The usual shields/vercel cards were dropped because the public instances
# are unreliable: github-readme-stats answers 503 under load and
# github-readme-activity-graph answers 402 once its Vercel quota is spent.
# A broken image on a profile is worse than no image, so the numbers are
# fetched in CI and drawn here instead, in the same language as the other
# figures, and served from this repository.
#
#   GITHUB_TOKEN=... python assets/stats.py [username]
import io
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

from generate import THEMES, MONO, SANS, CH, svg_open

OUT = os.path.dirname(os.path.abspath(__file__))
USER = sys.argv[1] if len(sys.argv) > 1 else "AhmadEbaid001"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

# languages that describe tooling rather than engineering, or that a single
# vendored file would otherwise push up the chart
LANG_SKIP = {"Batchfile", "Makefile", "Dockerfile", "Roff"}


def api(path):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"{USER}-profile-stats",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect():
    user = api(f"/users/{USER}")
    repos, page = [], 1
    while True:
        batch = api(f"/users/{USER}/repos?per_page=100&page={page}&type=owner")
        repos += batch
        if len(batch) < 100:
            break
        page += 1

    own = [r for r in repos if not r["fork"]]
    stars = sum(r["stargazers_count"] for r in own)

    langs = {}
    for r in own:
        try:
            for name, size in api(f"/repos/{USER}/{r['name']}/languages").items():
                if name not in LANG_SKIP:
                    langs[name] = langs.get(name, 0) + size
        except urllib.error.HTTPError:
            continue  # a repo can disappear between listing and lookup

    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
    total = sum(v for _, v in top) or 1
    return {
        "repos": user["public_repos"],
        "followers": user["followers"],
        # kept for the aria description even when it is not worth a figure
        "stars": stars,
        "since": user["created_at"][:4],
        "langs": [(n, v / total) for n, v in top],
    }


def render(t, d):
    W, H = 900, 232
    p = []
    a = p.append
    langs_desc = ", ".join(f"{n} {int(f*100)}%" for n, f in d["langs"])
    a(svg_open(W, H, f"GitHub statistics for {USER}: {d['repos']} public repositories, "
                     f"{d['followers']} followers, on GitHub since {d['since']}. "
                     f"Most used languages: {langs_desc}."))
    a(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')
    a(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" stroke="{t["line"]}"/>')
    a(f'<text x="34" y="34" font-family="{MONO}" font-size="10" letter-spacing="2.4" '
      f'fill="{t["subtle"]}">GITHUB</text>')
    a(f'<line x1="34" y1="46" x2="{W-34}" y2="46" stroke="{t["line"]}"/>')

    # a "0 stars" figure reads as a weakness rather than a fact, so the slot
    # goes to something that is always meaningful
    figures = [("PUBLIC REPOS", d["repos"]), ("FOLLOWERS", d["followers"]),
               ("LANGUAGES", len(d["langs"])), ("ON GITHUB SINCE", d["since"])]
    for i, (label, value) in enumerate(figures):
        x = 34 + i * 216
        a(f'<text x="{x}" y="70" font-family="{MONO}" font-size="9.5" letter-spacing="1.6" '
          f'fill="{t["subtle"]}">{label}</text>')
        a(f'<text x="{x}" y="106" font-family="{SANS}" font-size="34" font-weight="700" '
          f'letter-spacing="-1" fill="{t["fg"]}">{value}</text>')

    # language split as one stacked bar, widths animated in from the left
    bx, by, bw, bh = 34, 140, W - 68, 16
    a(f'<text x="{bx}" y="132" font-family="{MONO}" font-size="9.5" letter-spacing="1.6" '
      f'fill="{t["subtle"]}">LANGUAGE SPLIT</text>')
    shades = ["accent", "accent", "strong", "strong", "line", "line"]
    op = [1, 0.72, 1, 0.7, 1, 0.6]
    cursor = bx
    for i, (name, frac) in enumerate(d["langs"]):
        w = max(bw * frac, 2)
        a(f'<rect x="{cursor:.1f}" y="{by}" width="{w:.1f}" height="{bh}" '
          f'fill="{t[shades[i]]}" opacity="{op[i]}">'
          f'<animate attributeName="height" values="0;{bh}" dur="0.7s" '
          f'begin="{i*0.09:.2f}s" fill="freeze"/>'
          f'<animate attributeName="y" values="{by+bh};{by}" dur="0.7s" '
          f'begin="{i*0.09:.2f}s" fill="freeze"/></rect>')
        cursor += w

    lx = bx
    for i, (name, frac) in enumerate(d["langs"]):
        label = f"{name} {frac*100:.0f}%"
        a(f'<rect x="{lx}" y="{by+38}" width="8" height="8" fill="{t[shades[i]]}" '
          f'opacity="{op[i]}"/>')
        a(f'<text x="{lx+14}" y="{by+46}" font-family="{MONO}" font-size="10" '
          f'fill="{t["muted"]}">{label}</text>')
        lx += (len(label) + 4) * 10 * CH + 18

    stamp = datetime.now(timezone.utc).strftime("%d %b %Y")
    a(f'<text x="{W-34}" y="34" text-anchor="end" font-family="{MONO}" font-size="9.5" '
      f'letter-spacing="1.6" fill="{t["subtle"]}">MEASURED {stamp.upper()}</text>')
    a('</svg>')
    return "".join(p)


if __name__ == "__main__":
    data = collect()
    print(json.dumps(data, indent=2))
    for theme, tokens in THEMES.items():
        path = os.path.join(OUT, f"stats-{theme}.svg")
        io.open(path, "w", encoding="utf-8", newline="\n").write(render(tokens, data))
        print(f"wrote {os.path.basename(path):20} {os.path.getsize(path):>6} bytes")
