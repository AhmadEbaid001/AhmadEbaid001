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


# ---------------------------------------------------------------- badges ----
# Brand marks are the official GitHub and LinkedIn glyphs, used only as link
# icons. The rest are drawn here in the same stroke language as the other
# figures.
ICONS = {
    # Brand marks kept on ONE line each: splitting a path across adjacent
    # string literals silently joins the segments without a separator and
    # corrupts the coordinates, which turned the octocat into a crescent.
    "github": ("fill", "M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"),
    "linkedin": ("fill", "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"),
    "mail": ("fill", "M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"),
    "globe": ("stroke", "M12 3a9 9 0 100 18 9 9 0 000-18zM3.2 12h17.6M12 3.2a15 15 0 010 17.6M12 3.2a15 15 0 000 17.6"),
    "doc": ("stroke", "M7 3.2h6.6L18 7.6V20a.8.8 0 01-.8.8H7a.8.8 0 01-.8-.8V4a.8.8 0 01.8-.8zM13.2 3.4V8h4.6M9.4 13.2h5.2M9.4 16.6h5.2"),
}


def badge(t, icon, label, accent_icon=True):
    """One pill: brand mark plus label, sized to the text."""
    fs, h, pad, gap, isz = 11, 34, 13, 9, 15
    tw = len(label) * fs * CH + (len(label) - 1) * 1.4
    W = pad + isz + gap + tw + pad
    kind, d = ICONS[icon]
    col = t["accent"] if accent_icon else t["fg"]
    p = [svg_open(round(W), h, label)]
    a = p.append
    a(f'<rect x="0.5" y="0.5" width="{round(W)-1}" height="{h-1}" rx="3" '
      f'fill="{t["panel"]}" stroke="{t["strong"]}"/>')
    scale = isz / 24
    ty = (h - isz) / 2
    if kind == "fill":
        a(f'<g transform="translate({pad} {ty}) scale({scale:.4f})">'
          f'<path d="{d}" fill="{col}"/></g>')
    else:
        a(f'<g transform="translate({pad} {ty}) scale({scale:.4f})">'
          f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.8" '
          f'stroke-linecap="round" stroke-linejoin="round"/></g>')
    a(f'<text x="{pad + isz + gap}" y="{h/2 + 4}" font-family="{MONO}" font-size="{fs}" '
      f'letter-spacing="1.4" fill="{t["fg"]}">{label}</text>')
    a('</svg>')
    return "".join(p)


BADGES = [("portfolio", "globe", "PORTFOLIO"), ("linkedin", "linkedin", "LINKEDIN"),
          ("resume", "doc", "RESUME"), ("email", "mail", "EMAIL"),
          ("github", "github", "GITHUB")]


FIGURES = (("header", header), ("terminal", terminal),
           ("chain", chain), ("marquee", marquee))

if __name__ == "__main__":
    for name, fn in FIGURES:
        for theme, tokens in THEMES.items():
            path = os.path.join(OUT, f"{name}-{theme}.svg")
            io.open(path, "w", encoding="utf-8", newline="\n").write(fn(tokens))
            print(f"wrote {os.path.basename(path):24} {os.path.getsize(path):>6} bytes")

    for slug, icon, label in BADGES:
        for theme, tokens in THEMES.items():
            path = os.path.join(OUT, f"badge-{slug}-{theme}.svg")
            io.open(path, "w", encoding="utf-8", newline="\n").write(
                badge(tokens, icon, label))
            print(f"wrote {os.path.basename(path):24} {os.path.getsize(path):>6} bytes")
