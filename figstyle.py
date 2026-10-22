"""Shared visual style for the redesigned figures (HTML/CSS cards + inline
matplotlib SVG, rendered with Edge at 600 dpi for an 18 cm column)."""
import io
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)

WIDTH = 1400          # CSS px  -> 180 mm print width
SCALE = 3.1           # device pixels per CSS px -> ~4340 px (600 dpi at 18.4 cm)

NAVY, TEAL, BLUE, GREEN = "#1D3557", "#1F7A80", "#2E5E9E", "#4A8C3F"
GOLD, PURPLE, RED, GREY = "#C9861A", "#6B4FA0", "#C0392B", "#8A94A3"
TINT = {TEAL: "#E7F3F3", BLUE: "#E9EFF8", GREEN: "#EBF4E7", GOLD: "#FBF2E1",
        PURPLE: "#F0ECF7", RED: "#FBE9E7", NAVY: "#E6EAF1", GREY: "#F1F3F6"}
STEP_COL = {"HI": TEAL, "HC": BLUE, "EA": GREEN, "RC": GOLD}

plt.rcParams.update({
    "font.family": "Segoe UI",
    "font.size": 15,
    "axes.labelsize": 15,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 14,
    "axes.edgecolor": "#5B6676",
    "axes.labelcolor": "#1D2B3A",
    "xtick.color": "#3A4656",
    "ytick.color": "#3A4656",
    "text.color": "#1D2B3A",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "svg.fonttype": "none",
})

CSS = """
* { box-sizing: border-box; }
body { margin: 0; background: #fff; font-family: 'Segoe UI', Arial, sans-serif; color: #1D2B3A; }
#fig { width: %dpx; padding: 30px 22px 20px; background: #fff; }
.card { position: relative; border: 2.5px solid var(--c); border-radius: 18px; background: #fff;
        padding: 40px 20px 16px; }
.tag { position: absolute; top: 0; left: 50%%; transform: translate(-50%%, -50%%); background: var(--c);
       color: #fff; font-weight: 600; font-size: 23px; padding: 5px 22px; border-radius: 10px;
       white-space: nowrap; letter-spacing: .2px; }
.grid { display: grid; gap: 26px; }
svg { display: block; }
.note { font-size: 17px; color: #4A5565; }
""" % WIDTH


def svg_of(fig):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    return s


def card(color, tag, inner, style=""):
    return (f'<div class="card" style="--c:{color};{style}"><div class="tag">{tag}</div>'
            f'{inner}</div>')


def render(body, name, extra_css=""):
    html = f"<html><head><meta charset='utf-8'><style>{CSS}{extra_css}</style></head>" \
           f"<body><div id='fig'>{body}</div></body></html>"
    with open(os.path.join(OUT, f"_{name}.html"), "w", encoding="utf-8") as fh:
        fh.write(html)
    from playwright.sync_api import sync_playwright
    png = os.path.join(OUT, name + ".png")
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge")
        pg = b.new_page(viewport={"width": WIDTH + 40, "height": 900}, device_scale_factor=SCALE)
        pg.set_content(html)
        pg.wait_for_timeout(300)
        pg.query_selector("#fig").screenshot(path=png)
        b.close()
    finalize(png, name)


def finalize(png_path, name):
    im = Image.open(png_path).convert("RGB")
    im.save(os.path.join(OUT, name + ".png"), dpi=(600, 600))
    im.save(os.path.join(OUT, name + ".tif"), dpi=(600, 600), compression="tiff_lzw")
    print(f"saved {name}: {im.size[0]}x{im.size[1]} px")
