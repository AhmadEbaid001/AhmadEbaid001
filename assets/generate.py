# Generates the animated SVGs used by the profile README.
#
# Everything here is hand-authored and served from this repository, so the
# profile does not depend on a third-party badge service staying up.
#
# SMIL only, never <script>: GitHub serves README images through its camo
# proxy, which strips scripting but plays declarative animation. Two themes
# per figure; the README picks one with <picture> + prefers-color-scheme.
#
#   python assets/generate.py
import io
import os

OUT = os.path.dirname(os.path.abspath(__file__))

THEMES = {
    "dark": dict(bg="#030914", panel="#0F141C", grid="#0B1220", fg="#FFFFFF",
                 muted="#B5B4B3", subtle="#6A6D71", line="#1A1F28",
                 strong="#31363F", accent="#22CD6E", danger="#ED5374"),
    "light": dict(bg="#FFFFFF", panel="#F3F3F2", grid="#F7F7F6", fg="#030914",
                  muted="#31363F", subtle="#6A6D71", line="#EAEAE9",
                  strong="#DADAD8", accent="#10843E", danger="#8E1C33"),
}

MONO = "JetBrains Mono,ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "Space Grotesk,Segoe UI,Helvetica Neue,Arial,sans-serif"
CH = 0.6  # monospace advance width as a fraction of font-size


def svg_open(w, h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img" aria-label="{label}">')


# ---------------------------------------------------------------- header ----
def header(t):
    """Banner: identity plus the defence-in-depth pipeline, running live."""
    W, H = 900, 260
    lanes = [158, 186, 214]
    gates = [(400, "WAF"), (516, "TLS"), (632, "AUTHZ")]
    ox, ow = 712, 108

    p = []
    a = p.append
    a(svg_open(W, H, "Ahmed Mohamed Ebaid, cloud security engineer. Requests "
                     "flowing through WAF, TLS and authorisation gates into an origin."))
    a(f'<defs><pattern id="g" width="30" height="30" patternUnits="userSpaceOnUse">'
      f'<path d="M30 0H0V30" fill="none" stroke="{t["grid"]}"/></pattern></defs>')
    a(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')
    a(f'<rect width="{W}" height="{H}" fill="url(#g)"/>')
    a(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" stroke="{t["line"]}"/>')

    # a slow scan sweep, the only ambient motion in the identity block
    a(f'<rect x="0" y="0" width="150" height="{H}" fill="{t["accent"]}" opacity="0.03">'
      f'<animate attributeName="x" values="-150;{W}" dur="9s" repeatCount="indefinite"/></rect>')

    a(f'<rect x="40" y="42" width="12" height="12" fill="{t["accent"]}"/>')
    a(f'<text x="66" y="55" font-family="{SANS}" font-size="30" font-weight="700" '
      f'letter-spacing="-0.8" fill="{t["fg"]}">Ahmed Mohamed Ebaid</text>')
    a(f'<text x="66" y="81" font-family="{MONO}" font-size="12" letter-spacing="3.4" '
      f'fill="{t["accent"]}">CLOUD SECURITY ENGINEER</text>')
    a(f'<rect x="371" y="70" width="8" height="14" fill="{t["accent"]}">'
      f'<animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/></rect>')

    for i, txt in enumerate(("GIZA, EGYPT", "B.SC. CSAI &#183; ZEWAIL CITY",
                             "OPEN TO CLOUD SECURITY ROLES")):
        a(f'<text x="860" y="{50 + i*17}" text-anchor="end" font-family="{MONO}" '
          f'font-size="10" letter-spacing="1.6" fill="{t["subtle"]}">{txt}</text>')

    a(f'<line x1="40" y1="108" x2="860" y2="108" stroke="{t["line"]}"/>')
    a(f'<text x="40" y="132" font-family="{MONO}" font-size="10" letter-spacing="2.4" '
      f'fill="{t["subtle"]}">DEFENCE IN DEPTH</text>')
    a(f'<text x="860" y="132" text-anchor="end" font-family="{MONO}" font-size="10" '
      f'letter-spacing="2.4" fill="{t["accent"]}">ALL GATES UP</text>')

    for y in lanes:
        a(f'<line x1="60" y1="{y}" x2="{ox-12}" y2="{y}" stroke="{t["strong"]}"/>')

    for gx, label in gates:
        a(f'<line x1="{gx}" y1="146" x2="{gx}" y2="228" stroke="{t["strong"]}" stroke-width="2"/>')
        a(f'<text x="{gx}" y="140" text-anchor="middle" font-family="{MONO}" font-size="9" '
          f'letter-spacing="1.4" fill="{t["subtle"]}">{label}</text>')

    a(f'<rect x="{ox}" y="150" width="{ow}" height="78" fill="{t["panel"]}" stroke="{t["strong"]}"/>')
    a(f'<text x="{ox+ow/2}" y="140" text-anchor="middle" font-family="{MONO}" font-size="9" '
      f'letter-spacing="1.4" fill="{t["subtle"]}">ORIGIN</text>')

    served = [(lanes[0], 0.0, 4.6), (lanes[1], 1.5, 5.1), (lanes[2], 0.7, 4.3),
              (lanes[0], 2.9, 4.6), (lanes[2], 3.4, 4.3), (lanes[1], 4.1, 5.1)]
    for y, delay, dur in served:
        a(f'<rect width="8" height="8" y="{y-4}" x="-10" fill="{t["accent"]}">'
          f'<animate attributeName="x" values="56;{ox-16}" dur="{dur}s" begin="{delay}s" '
          f'repeatCount="indefinite"/></rect>')

    blocked = [(lanes[1], gates[0][0], 0.4, 2.6), (lanes[2], gates[1][0], 2.1, 3.4),
               (lanes[0], gates[2][0], 1.3, 4.0)]
    for y, gx, delay, dur in blocked:
        a(f'<g><rect width="8" height="8" y="{y-4}" x="-10" fill="{t["danger"]}">'
          f'<animate attributeName="x" values="56;{gx-9}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.88;0.94;1" dur="{dur}s" '
          f'begin="{delay}s" repeatCount="indefinite"/></rect>'
          f'<g stroke="{t["danger"]}" stroke-width="1.4" opacity="0">'
          f'<line x1="{gx-13}" y1="{y-4}" x2="{gx-5}" y2="{y+4}"/>'
          f'<line x1="{gx-5}" y1="{y-4}" x2="{gx-13}" y2="{y+4}"/>'
          f'<animate attributeName="opacity" values="0;0;1;0" keyTimes="0;0.88;0.93;1" dur="{dur}s" '
          f'begin="{delay}s" repeatCount="indefinite"/></g></g>')

    a(f'<text x="860" y="248" text-anchor="end" font-family="{MONO}" font-size="9" '
      f'letter-spacing="1.4" fill="{t["subtle"]}">SWITCH A GATE OFF AND THAT CLASS WALKS IN</text>')
    a('</svg>')
    return "".join(p)


# -------------------------------------------------------------- terminal ----
def terminal(t):
    """A session that types itself out, loops, and says something true."""
    W, H = 900, 372
    fs, lh, x0, y0 = 13.5, 26, 34, 62
    lines = [
        ("cmd", "whoami"),
        ("out", "ahmed-ebaid  &#183;  cloud security engineer  &#183;  giza, egypt"),
        ("gap", ""),
        ("cmd", "cat focus.txt"),
        ("out", "hybrid cloud architecture &#183; tamper-evident systems &#183; devsecops"),
        ("gap", ""),
        ("cmd", "aura --status"),
        ("ok", "pre-incubation   5,000 users   902,246 reqs   p95 299ms   $3.50/mo"),
        ("gap", ""),
        ("cmd", "gemp --verify-chain"),
        ("ok", "457 tests green   chain head anchored   walk 01..05 ok"),
    ]

    # One pass, then freeze. A looping reveal means the panel is blank for
    # part of every cycle, and anything that stops the animation (a renderer
    # that ignores SMIL, a paused tab, an image re-decode) can leave it blank
    # for good. Typing once and freezing on the finished session cannot.
    slots = [i for i, (k, _) in enumerate(lines) if k != "gap"]
    per = 0.5
    total = len(slots) * per + 0.6

    p = []
    a = p.append
    a(svg_open(W, H, "Terminal session: whoami, focus, AURA status and GEMP chain verification."))
    a(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')
    a(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" stroke="{t["line"]}"/>')
    a(f'<text x="{x0}" y="30" font-family="{MONO}" font-size="10" letter-spacing="2.2" '
      f'fill="{t["subtle"]}">~/ahmed &#8212; zsh</text>')
    a(f'<line x1="{x0}" y1="42" x2="{W-x0}" y2="42" stroke="{t["line"]}"/>')

    slot_i = 0
    for i, (kind, text) in enumerate(lines):
        if kind == "gap":
            continue
        y = y0 + i * lh
        begin = slot_i * per
        t0 = begin / total
        t1 = (begin + per * 0.5) / total
        prompt_w = 2 * fs * CH if kind == "cmd" else 0
        text_w = len(text.replace("&#183;", "-").replace("&#8212;", "-")) * fs * CH
        total_w = prompt_w + text_w

        # No animation on the text itself. Once an <animate> exists, its value
        # at t=0 overrides the static attribute -- and when this SVG is embedded
        # as <img> (which is how GitHub renders README images) some renderers
        # never advance the clock, so an opacity-0 first frame means the panel
        # stays blank permanently. The text is therefore always painted; the
        # caret below carries the motion, and losing a caret costs nothing.
        fill = {"cmd": t["fg"], "out": t["muted"], "ok": t["accent"]}[kind]

        a('<g>')
        if kind == "cmd":
            a(f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{fs}" '
              f'fill="{t["accent"]}">$ </text>')
            a(f'<text x="{x0+prompt_w}" y="{y}" font-family="{MONO}" font-size="{fs}" '
              f'fill="{fill}">{text}</text>')
        else:
            marker = "&#8226; " if kind == "ok" else ""
            a(f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{fs}" '
              f'fill="{fill}">{marker}{text}</text>')
        a('</g>')
        slot_i += 1

    # the session rests with a blinking caret; its first frame is "on", so a
    # frozen clock leaves a solid caret rather than nothing
    ylast = y0 + len(lines) * lh
    a(f'<rect x="{x0}" y="{ylast-fs+2}" width="8" height="{fs+1}" fill="{t["accent"]}">'
      f'<animate attributeName="opacity" values="1;1;0;0" dur="1.1s" '
      f'repeatCount="indefinite"/></rect>')
    a('</svg>')
    return "".join(p)


# ----------------------------------------------------------------- chain ----
def chain(t):
    """Slim divider: a verify walk travelling along a hash chain."""
    n, x0, gap, size = 6, 24, 96, 26
    p = []
    a = p.append
    a(svg_open(620, 60, "A hash chain of six signed records being verified end to end."))
    a(f'<rect width="620" height="60" fill="{t["bg"]}"/>')
    for i in range(n):
        x = x0 + i * gap
        if i < n - 1:
            a(f'<line x1="{x+size}" y1="30" x2="{x+gap}" y2="30" stroke="{t["strong"]}"/>')
        a(f'<rect x="{x}" y="17" width="{size}" height="{size}" fill="{t["panel"]}" stroke="{t["strong"]}"/>')

    period = n * 0.55 + 1.2
    for i in range(n):
        a(f'<rect x="{x0+i*gap}" y="17" width="{size}" height="{size}" fill="none" '
          f'stroke="{t["accent"]}" stroke-width="2" opacity="0">'
          f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.06;0.72;1" '
          f'dur="{period}s" begin="{i*0.55}s" repeatCount="indefinite"/></rect>')

    a(f'<text x="596" y="34" text-anchor="end" font-family="{MONO}" font-size="9.5" '
      f'letter-spacing="1.6" fill="{t["subtle"]}" opacity="0">HEAD OK'
      f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.62;0.7;0.92;1" '
      f'dur="{period}s" repeatCount="indefinite"/></text>')
    a('</svg>')
    return "".join(p)


# --------------------------------------------------------------- marquee ----
def marquee(t):
    """A continuously scrolling strip of the stack, in two opposed rows."""
    W, H, fs = 900, 96, 12
    rows = [
        ["AWS", "AZURE", "DOCKER", "HAPROXY", "NGINX", "WIREGUARD", "CLOUDFLARE",
         "GITHUB ACTIONS", "POSTGRESQL", "TIMESCALEDB", "REDIS", "LINUX"],
        ["SEMGREP", "BANDIT", "TRIVY", "GITLEAKS", "NESSUS", "SPLUNK", "WIRESHARK",
         "VOLATILITY", "NMAP", "SNORT", "AUTOPSY"],
    ]
    p = []
    a = p.append
    a(svg_open(W, H, "Scrolling list of tools: cloud and infrastructure on the top row, "
                     "security tooling on the bottom row."))
    a(f'<defs><linearGradient id="fade" x1="0" x2="1">'
      f'<stop offset="0" stop-color="{t["bg"]}"/><stop offset="0.08" stop-color="{t["bg"]}" stop-opacity="0"/>'
      f'<stop offset="0.92" stop-color="{t["bg"]}" stop-opacity="0"/><stop offset="1" stop-color="{t["bg"]}"/>'
      f'</linearGradient></defs>')
    a(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')

    for r, items in enumerate(rows):
        y = 36 + r * 34
        # doubling the sequence makes the wrap seamless
        seq = items + items
        widths, xs, cur = [], [], 0
        for it in seq:
            w = len(it) * fs * CH + 26
            widths.append(w)
            xs.append(cur)
            cur += w
        span = cur / 2
        dur = 26 + r * 6
        frm, to = (0, -span) if r == 0 else (-span, 0)

        a(f'<g><animateTransform attributeName="transform" type="translate" '
          f'from="{frm} 0" to="{to} 0" dur="{dur}s" repeatCount="indefinite"/>')
        for it, x, w in zip(seq, xs, widths):
            a(f'<rect x="{x:.1f}" y="{y-15}" width="{w-12:.1f}" height="24" fill="none" '
              f'stroke="{t["line"]}"/>')
            a(f'<text x="{x+ (w-12)/2:.1f}" y="{y+1}" text-anchor="middle" font-family="{MONO}" '
              f'font-size="{fs}" letter-spacing="1.4" fill="{t["muted"]}">{it}</text>')
        a('</g>')

    a(f'<rect width="{W}" height="{H}" fill="url(#fade)"/>')
    a('</svg>')
    return "".join(p)


FIGURES = (("header", header), ("terminal", terminal),
           ("chain", chain), ("marquee", marquee))

if __name__ == "__main__":
    for name, fn in FIGURES:
        for theme, tokens in THEMES.items():
            path = os.path.join(OUT, f"{name}-{theme}.svg")
            io.open(path, "w", encoding="utf-8", newline="\n").write(fn(tokens))
            print(f"wrote {os.path.basename(path):24} {os.path.getsize(path):>6} bytes")
