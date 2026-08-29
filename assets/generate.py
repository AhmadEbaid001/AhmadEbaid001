# Generates the animated SVGs for the GitHub profile README.
# Two themes per figure; GitHub picks one via <picture> + prefers-color-scheme.
# SMIL only — no scripts, since GitHub proxies images through camo.
import io, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(OUT, exist_ok=True)

THEMES = {
    "dark":  dict(bg="#030914", panel="#0F141C", fg="#FFFFFF", muted="#B5B4B3",
                  subtle="#6A6D71", line="#1A1F28", strong="#31363F",
                  accent="#22CD6E", danger="#ED5374"),
    "light": dict(bg="#FFFFFF", panel="#F3F3F2", fg="#030914", muted="#31363F",
                  subtle="#6A6D71", line="#EAEAE9", strong="#DADAD8",
                  accent="#10843E", danger="#8E1C33"),
}

MONO = "JetBrains Mono,ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "Space Grotesk,Segoe UI,Helvetica Neue,Arial,sans-serif"


def header(t):
    """Banner: name, role, and a live request pipeline through three gates."""
    lanes = [140, 164, 188]
    gates = [(392, "WAF"), (508, "TLS"), (624, "AUTHZ")]
    ox, ow = 706, 108

    p = []
    a = p.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 232" width="900" height="232" '
      f'role="img" aria-label="Ahmed Mohamed Ebaid, cloud security engineer. Requests flowing '
      f'through WAF, TLS and authorisation gates into an origin.">')
    a(f'<rect width="900" height="232" fill="{t["bg"]}"/>')
    a(f'<rect x="0.5" y="0.5" width="899" height="231" fill="none" stroke="{t["line"]}"/>')

    # --- identity block ---
    a(f'<rect x="40" y="40" width="11" height="11" fill="{t["accent"]}"/>')
    a(f'<text x="64" y="52" font-family="{SANS}" font-size="27" font-weight="700" '
      f'letter-spacing="-0.6" fill="{t["fg"]}">Ahmed Mohamed Ebaid</text>')
    a(f'<text x="64" y="76" font-family="{MONO}" font-size="11.5" letter-spacing="3" '
      f'fill="{t["accent"]}">CLOUD SECURITY ENGINEER</text>')
    # blinking cursor after the role
    a(f'<rect x="284" y="66" width="7" height="13" fill="{t["accent"]}">'
      f'<animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/></rect>')

    a(f'<text x="860" y="52" text-anchor="end" font-family="{MONO}" font-size="10" '
      f'letter-spacing="1.6" fill="{t["subtle"]}">GIZA, EGYPT</text>')
    a(f'<text x="860" y="70" text-anchor="end" font-family="{MONO}" font-size="10" '
      f'letter-spacing="1.6" fill="{t["subtle"]}">B.SC. CSAI &#183; ZEWAIL CITY</text>')

    a(f'<line x1="40" y1="98" x2="860" y2="98" stroke="{t["line"]}"/>')
    a(f'<text x="40" y="120" font-family="{MONO}" font-size="10" letter-spacing="2.2" '
      f'fill="{t["subtle"]}">DEFENCE IN DEPTH</text>')

    # --- lanes ---
    for y in lanes:
        a(f'<line x1="60" y1="{y}" x2="{ox - 12}" y2="{y}" stroke="{t["strong"]}"/>')

    # --- gates ---
    for gx, label in gates:
        a(f'<line x1="{gx}" y1="126" x2="{gx}" y2="202" stroke="{t["strong"]}" stroke-width="2"/>')
        a(f'<text x="{gx}" y="118" text-anchor="middle" font-family="{MONO}" font-size="9" '
          f'letter-spacing="1.4" fill="{t["subtle"]}">{label}</text>')

    # --- origin ---
    a(f'<rect x="{ox}" y="128" width="{ow}" height="72" fill="{t["panel"]}" stroke="{t["strong"]}"/>')
    a(f'<text x="{ox + ow / 2}" y="118" text-anchor="middle" font-family="{MONO}" font-size="9" '
      f'letter-spacing="1.4" fill="{t["subtle"]}">ORIGIN</text>')

    # --- traffic: green requests cross, red ones die at their gate ---
    served = [(lanes[0], 0.0, 4.6), (lanes[1], 1.5, 5.1), (lanes[2], 0.7, 4.3),
              (lanes[0], 2.9, 4.6), (lanes[2], 3.4, 4.3)]
    for y, delay, dur in served:
        a(f'<rect width="8" height="8" y="{y - 4}" fill="{t["accent"]}" x="-10">'
          f'<animate attributeName="x" values="56;{ox - 16}" dur="{dur}s" '
          f'begin="{delay}s" repeatCount="indefinite"/></rect>')

    blocked = [(lanes[1], gates[0][0], 0.4, 2.6), (lanes[2], gates[1][0], 2.1, 3.4),
               (lanes[0], gates[2][0], 1.3, 4.0)]
    for y, gx, delay, dur in blocked:
        a(f'<g>'
          f'<rect width="8" height="8" y="{y - 4}" fill="{t["danger"]}" x="-10">'
          f'<animate attributeName="x" values="56;{gx - 9}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.88;0.94;1" dur="{dur}s" '
          f'begin="{delay}s" repeatCount="indefinite"/></rect>'
          # the ✕ that marks the block
          f'<g stroke="{t["danger"]}" stroke-width="1.4" opacity="0">'
          f'<line x1="{gx - 13}" y1="{y - 4}" x2="{gx - 5}" y2="{y + 4}"/>'
          f'<line x1="{gx - 5}" y1="{y - 4}" x2="{gx - 13}" y2="{y + 4}"/>'
          f'<animate attributeName="opacity" values="0;0;1;0" keyTimes="0;0.88;0.93;1" dur="{dur}s" '
          f'begin="{delay}s" repeatCount="indefinite"/></g>'
          f'</g>')

    a(f'<text x="860" y="222" text-anchor="end" font-family="{MONO}" font-size="9" '
      f'letter-spacing="1.4" fill="{t["subtle"]}">SWITCH A GATE OFF AND THAT CLASS WALKS IN</text>')
    a('</svg>')
    return "".join(p)


def chain(t):
    """Slim divider: a verify walk travelling along a hash chain."""
    n, x0, gap, size = 6, 24, 96, 26
    p = []
    a = p.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 60" width="620" height="60" '
      f'role="img" aria-label="A hash chain of six signed records being verified end to end.">')
    a(f'<rect width="620" height="60" fill="{t["bg"]}"/>')

    for i in range(n):
        x = x0 + i * gap
        if i < n - 1:
            a(f'<line x1="{x + size}" y1="30" x2="{x + gap}" y2="30" stroke="{t["strong"]}"/>')
        a(f'<rect x="{x}" y="17" width="{size}" height="{size}" fill="{t["panel"]}" stroke="{t["strong"]}"/>')

    # the walk: a green pulse steps record to record, then the chain reads verified
    period = n * 0.55 + 1.2
    for i in range(n):
        x = x0 + i * gap
        begin = i * 0.55
        a(f'<rect x="{x}" y="17" width="{size}" height="{size}" fill="none" stroke="{t["accent"]}" '
          f'stroke-width="2" opacity="0">'
          f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.06;0.72;1" '
          f'dur="{period}s" begin="{begin}s" repeatCount="indefinite"/></rect>')

    a(f'<text x="596" y="34" text-anchor="end" font-family="{MONO}" font-size="9.5" '
      f'letter-spacing="1.6" fill="{t["subtle"]}" opacity="0">HEAD OK'
      f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.62;0.7;0.92;1" '
      f'dur="{period}s" repeatCount="indefinite"/></text>')
    a('</svg>')
    return "".join(p)


for name, fn in (("header", header), ("chain", chain)):
    for theme, tokens in THEMES.items():
        path = os.path.join(OUT, f"{name}-{theme}.svg")
        io.open(path, "w", encoding="utf-8", newline="\n").write(fn(tokens))
        print("wrote", path, os.path.getsize(path), "bytes")
