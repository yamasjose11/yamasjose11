"""Generate the profile SVG assets (dark + light) from one source of truth.

Run:  python scripts/build_assets.py
Edit the CONTENT dicts below, rerun, commit. No dependencies.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": {
        "bg": "#0d1117", "card": "#111720", "border": "#252c36", "grid": "#1b222c",
        "fg": "#e6edf3", "fg2": "#b4bdc8", "muted": "#7d8794",
        "accent": "#f0a33a", "accent_soft": "#f0a33a33",
    },
    "light": {
        "bg": "#ffffff", "card": "#f8f9fb", "border": "#d8dee6", "grid": "#eef1f5",
        "fg": "#1a1f26", "fg2": "#3d4652", "muted": "#6b7480",
        "accent": "#b86a00", "accent_soft": "#b86a0022",
    },
}

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

# ---------------------------------------------------------------- content
HEADER = {
    "eyebrow": "AGENTIC SYSTEMS  /  DATA PLATFORMS  /  OPS AUTOMATION",
    "name": "Yamas",
    "title": "Full Stack Agentic AI Engineer",
    "thesis": "I build agentic systems that replace spreadsheets, forms and email chains",
    "thesis2": "with governed, auditable automation.",
    "pipeline": [
        ("01", "intake", "forms · email · systems"),
        ("02", "reason", "models"),
        ("03", "act", "tools · agents"),
        ("04", "validate", "tests · audit · pii"),
        ("05", "ship", "cloud"),
    ],
}

TERMINAL = [
    ("$ agent run ops.reconcile", None),
    ("  read     5 source systems", "ok"),
    ("  guard    pii tier check", "ok"),
    ("  verify   30/30 sample match", "ok"),
    ("  ship     human-approved", "done"),
]

STATS = [
    ("190×", "faster records audit", "160 ms vs 30 s per record"),
    ("~29 h", "saved per audit run", "3,641 records · 0 errors"),
    ("3 → 1", "tools consolidated", "sheets · forms · email → hub"),
    ("35+", "governed agent skills", "pii tiers · scope-lock hooks"),
]

VISION = {
    "label": "VISION BOARD  ·  2026 → 2027",
    "cols": [
        ("NOW", "building", "Platform sync", ["two live platforms", "kept in step"]),
        ("NEXT", "next", "Unified data platform", ["every tool feeds it,", "read-only"]),
        ("Q1 2027", "next", "System cutover", ["core system migration,", "history preserved"]),
        ("2027", "planned", "Open network", ["outside partners on", "live demand"]),
    ],
    "north": "Every recurring ops workflow runs agent-first and human-approved.",
}


# ---------------------------------------------------------------- helpers
def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg_open(w: int, h: int, title: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>')


def frame(t, w, h, grid=False) -> str:
    out = ""
    if grid:
        out += (f'<defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse">'
                f'<circle cx="1" cy="1" r="1" fill="{t["grid"]}"/></pattern></defs>')
    out += f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>'
    if grid:
        out += f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="14" fill="url(#g)"/>'
    return out


# ---------------------------------------------------------------- header
def header(t) -> str:
    W, H = 1000, 340
    xs = [90, 295, 500, 705, 910]
    ly = 262
    cycle = 6.0
    travel = 0.82  # share of the cycle the pulse spends moving
    css = f"""<style>
.blink{{animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{50%{{fill-opacity:0}}}}
.dot{{animation:dot 2.4s ease-in-out infinite;transform-origin:56px 59px}}
@keyframes dot{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
.pulse{{animation:run {cycle}s linear infinite}}
@keyframes run{{0%{{transform:translateX(0);opacity:0}}4%{{opacity:1}}{travel*100:.0f}%{{transform:translateX({xs[-1]-xs[0]}px);opacity:1}}{travel*100+6:.0f}%,100%{{transform:translateX({xs[-1]-xs[0]}px);opacity:0}}}}
.trail{{stroke-dasharray:{xs[-1]-xs[0]};stroke-dashoffset:{xs[-1]-xs[0]};animation:trail {cycle}s linear infinite}}
@keyframes trail{{0%{{stroke-dashoffset:{xs[-1]-xs[0]};opacity:1}}{travel*100:.0f}%{{stroke-dashoffset:0;opacity:1}}{travel*100+8:.0f}%,100%{{stroke-dashoffset:0;opacity:0}}}}
.node{{animation:lit {cycle}s linear infinite}}
@keyframes lit{{0%{{fill:{t["accent"]}}}10%,100%{{fill:{t["bg"]}}}}}
.ln{{animation:ln 9s ease-out infinite both}}
@keyframes ln{{0%{{opacity:0;transform:translateY(4px)}}4%{{opacity:1;transform:none}}80%{{opacity:1}}88%,100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.blink,.dot,.pulse,.trail,.node,.ln{{animation:none}}.trail{{stroke-dashoffset:0}}}}
</style>"""
    s = svg_open(W, H, f'{HEADER["name"]}, {HEADER["title"]}') + css + frame(t, W, H, grid=True)
    # eyebrow
    s += f'<circle class="dot" cx="56" cy="59" r="4" fill="{t["accent"]}"/>'
    s += (f'<text x="72" y="64" font-family="{MONO}" font-size="12.5" letter-spacing="1.6" '
          f'fill="{t["muted"]}">{esc(HEADER["eyebrow"])}</text>')
    # name + title
    s += (f'<text x="52" y="128" font-family="{SANS}" font-size="54" font-weight="700" letter-spacing="-1.2" '
          f'fill="{t["fg"]}">{esc(HEADER["name"])}</text>')
    s += (f'<text x="54" y="168" font-family="{SANS}" font-size="25" font-weight="500" fill="{t["fg2"]}">'
          f'{esc(HEADER["title"])}<tspan class="blink" fill="{t["accent"]}" font-family="{MONO}" dx="6">_</tspan></text>')
    s += (f'<text x="54" y="202" font-family="{SANS}" font-size="15" fill="{t["muted"]}">{esc(HEADER["thesis"])}'
          f'<tspan x="54" dy="21">{esc(HEADER["thesis2"])}</tspan></text>')
    # terminal card
    tx, ty, tw, th = 610, 40, 350, 178
    s += f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="10" fill="{t["card"]}" stroke="{t["border"]}"/>'
    for k, c in enumerate((t["border"], t["border"], t["border"])):
        s += f'<circle cx="{tx+18+k*14}" cy="{ty+18}" r="4" fill="{c}"/>'
    s += (f'<text x="{tx+tw-16}" y="{ty+22}" text-anchor="end" font-family="{MONO}" font-size="11" '
          f'fill="{t["muted"]}">agent.log</text>')
    s += f'<line x1="{tx}" y1="{ty+34}" x2="{tx+tw}" y2="{ty+34}" stroke="{t["border"]}"/>'
    for k, (line, status) in enumerate(TERMINAL):
        y = ty + 62 + k * 24
        col = t["fg"] if status is None else t["fg2"]
        s += (f'<g class="ln" style="animation-delay:{k*0.9:.1f}s"><text x="{tx+18}" y="{y}" font-family="{MONO}" '
              f'font-size="12" fill="{col}" xml:space="preserve">{esc(line)}</text>')
        if status:
            s += (f'<text x="{tx+tw-18}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="12" '
                  f'fill="{t["accent"]}">{status}</text>')
        s += '</g>'
    # pipeline
    s += f'<line x1="{xs[0]}" y1="{ly}" x2="{xs[-1]}" y2="{ly}" stroke="{t["border"]}" stroke-width="2"/>'
    s += (f'<line class="trail" x1="{xs[0]}" y1="{ly}" x2="{xs[-1]}" y2="{ly}" stroke="{t["accent"]}" '
          f'stroke-width="2" stroke-linecap="round"/>')
    for i, (x, (num, label, sub)) in enumerate(zip(xs, HEADER["pipeline"])):
        delay = cycle * travel * i / (len(xs) - 1)
        s += (f'<circle class="node" style="animation-delay:{delay:.2f}s" cx="{x}" cy="{ly}" r="7" '
              f'fill="{t["bg"]}" stroke="{t["accent"]}" stroke-width="2"/>')
        s += (f'<text x="{x}" y="{ly+32}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t["fg"]}">'
              f'<tspan fill="{t["muted"]}">{num}</tspan><tspan dx="7">{esc(label)}</tspan></text>')
        s += (f'<text x="{x}" y="{ly+52}" text-anchor="middle" font-family="{MONO}" font-size="11" '
              f'fill="{t["muted"]}">{esc(sub)}</text>')
    s += (f'<circle class="pulse" cx="{xs[0]}" cy="{ly}" r="10" fill="{t["accent_soft"]}"/>'
          f'<circle class="pulse" cx="{xs[0]}" cy="{ly}" r="4" fill="{t["accent"]}"/>')
    return s + "</svg>"


# ---------------------------------------------------------------- stats
def stats(t) -> str:
    W, H = 1000, 150
    s = svg_open(W, H, "Victories and savings") + frame(t, W, H)
    cw = W / len(STATS)
    for i, (big, label, cap) in enumerate(STATS):
        x = i * cw + 30
        if i:
            s += f'<line x1="{i*cw:.0f}" y1="28" x2="{i*cw:.0f}" y2="{H-28}" stroke="{t["border"]}"/>'
        s += f'<rect x="{x}" y="30" width="22" height="3" rx="1.5" fill="{t["accent"]}"/>'
        s += (f'<text x="{x}" y="78" font-family="{SANS}" font-size="36" font-weight="700" letter-spacing="-0.8" '
              f'fill="{t["fg"]}">{esc(big)}</text>')
        s += f'<text x="{x}" y="102" font-family="{SANS}" font-size="14" fill="{t["fg2"]}">{esc(label)}</text>'
        s += f'<text x="{x}" y="122" font-family="{MONO}" font-size="11" fill="{t["muted"]}">{esc(cap)}</text>'
    return s + "</svg>"


# ---------------------------------------------------------------- vision
def vision(t) -> str:
    W, H = 1000, 312
    s = svg_open(W, H, "Vision board 2026 to 2027") + frame(t, W, H)
    s += (f'<text x="40" y="46" font-family="{MONO}" font-size="12.5" letter-spacing="1.6" '
          f'fill="{t["muted"]}">{esc(VISION["label"])}</text>')
    pad, gap, n = 40, 16, len(VISION["cols"])
    cw = (W - 2 * pad - gap * (n - 1)) / n
    top, ch = 70, 150
    # rail
    s += f'<line x1="{pad}" y1="{top-6}" x2="{W-pad}" y2="{top-6}" stroke="{t["border"]}"/>'
    for i, (when, status, head, lines) in enumerate(VISION["cols"]):
        x = pad + i * (cw + gap)
        s += f'<circle cx="{x+12}" cy="{top-6}" r="3.5" fill="{t["accent"] if status != "planned" else t["muted"]}"/>'
        s += f'<rect x="{x}" y="{top+6}" width="{cw:.1f}" height="{ch}" rx="10" fill="{t["card"]}" stroke="{t["border"]}"/>'
        s += (f'<text x="{x+18}" y="{top+34}" font-family="{MONO}" font-size="12" font-weight="600" '
              f'fill="{t["fg2"]}">{esc(when)}</text>')
        # chip
        chip_w = 8 + len(status) * 7.2
        cx = x + cw - 18 - chip_w
        if status == "building":
            s += f'<rect x="{cx:.1f}" y="{top+20}" width="{chip_w:.1f}" height="20" rx="10" fill="{t["accent"]}"/>'
            chip_fill = t["bg"]
        else:
            col = t["accent"] if status == "next" else t["muted"]
            s += (f'<rect x="{cx+0.5:.1f}" y="{top+20.5}" width="{chip_w-1:.1f}" height="19" rx="9.5" '
                  f'fill="none" stroke="{col}"/>')
            chip_fill = col
        s += (f'<text x="{cx+chip_w/2:.1f}" y="{top+34}" text-anchor="middle" font-family="{MONO}" '
              f'font-size="11" fill="{chip_fill}">{esc(status)}</text>')
        s += (f'<text x="{x+18}" y="{top+76}" font-family="{SANS}" font-size="17" font-weight="600" '
              f'fill="{t["fg"]}">{esc(head)}</text>')
        for j, line in enumerate(lines):
            s += (f'<text x="{x+18}" y="{top+104+j*19}" font-family="{MONO}" font-size="11.5" '
                  f'fill="{t["muted"]}">{esc(line)}</text>')
    # north star
    ny = top + ch + 32
    s += f'<rect x="{pad}" y="{ny}" width="{W-2*pad}" height="44" rx="10" fill="none" stroke="{t["border"]}"/>'
    s += f'<rect x="{pad}" y="{ny}" width="4" height="44" rx="2" fill="{t["accent"]}"/>'
    s += (f'<text x="{pad+22}" y="{ny+27}" font-family="{MONO}" font-size="12" letter-spacing="1.4" '
          f'fill="{t["accent"]}">NORTH STAR</text>')
    s += (f'<text x="{pad+136}" y="{ny+27}" font-family="{SANS}" font-size="15" '
          f'fill="{t["fg"]}">{esc(VISION["north"])}</text>')
    return s + "</svg>"


def main():
    OUT.mkdir(exist_ok=True)
    for name, fn in (("header", header), ("stats", stats), ("vision", vision)):
        for theme, t in THEMES.items():
            (OUT / f"{name}-{theme}.svg").write_text(fn(t), encoding="utf-8")
    print("assets written to", OUT)


if __name__ == "__main__":
    main()
