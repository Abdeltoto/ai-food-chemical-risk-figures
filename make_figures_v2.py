"""Reproduce Figures 2, 3, 8, 10, 11, 14 and 15 of the review
'Artificial intelligence for food chemical risk assessment and prioritization'.

    python make_figures_v2.py
    python make_figures_v2.py 2 3
"""
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
from corpus_coding import CODING, STEPS, FAMILIES, FAMILY_LABELS
from figstyle import (NAVY, TEAL, BLUE, GREEN, GOLD, PURPLE, RED, GREY, TINT, STEP_COL,
                      svg_of, card, render)

TYPE_COL = {"P": BLUE, "R": GOLD, "D": GREEN, "G": PURPLE}


# ------------------------------------------------------------ Figure 2
FLOW_CSS = """
.flow { display: grid; grid-template-columns: 1fr 34px 0.78fr; row-gap: 0; align-items: center; }
.fb { border-radius: 12px; padding: 12px 14px; text-align: center; font-size: 19px; line-height: 1.3;
      background: #E7F3F3; border: 1.5px solid #1F7A80; }
.fb b { display: block; font-size: 30px; color: #1F7A80; line-height: 1.1; }
.fb.x { background: #F1F3F6; border-color: #8A94A3; } .fb.x b { color: #5B6676; }
.fb.s { background: #F0ECF7; border-color: #6B4FA0; } .fb.s b { color: #6B4FA0; }
.fb.f { background: #EBF4E7; border-color: #4A8C3F; border-width: 2px; } .fb.f b { color: #3B7A31; font-size: 34px; }
.down { height: 30px; position: relative; }
.down::before { content: ''; position: absolute; left: 50%; top: 0; bottom: 9px; border-left: 2.5px solid #5B6676; }
.down::after { content: ''; position: absolute; left: calc(50% - 7px); bottom: 0; border: 7px solid transparent;
               border-top: 10px solid #5B6676; border-bottom: 0; }
.right, .left { height: 2.5px; background: #5B6676; position: relative; margin: 0 4px; }
.right::after { content: ''; position: absolute; right: -2px; top: -7px; border: 8px solid transparent;
                border-left: 11px solid #5B6676; border-right: 0; }
.left::after { content: ''; position: absolute; left: -2px; top: -7px; border: 8px solid transparent;
               border-right: 11px solid #5B6676; border-left: 0; }
.chips { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 10px; }
.chip { border-radius: 8px; color: #fff; font-size: 16px; padding: 4px 6px; font-weight: 600; }
"""


def figure2():
    tc = {t: sum(1 for v in CODING.values() if v[1] == t) for t in "PRDG"}
    chips = "".join(
        f'<div class="chip" style="background:{TYPE_COL[t]}">{tc[t]} {lab}</div>'
        for t, lab in [("P", "primary studies"), ("R", "reviews or surveys"),
                       ("D", "databases or resources"), ("G", "reports or governance")])
    flow = f"""
<div class="flow">
  <div class="fb"><b>961</b>records retrieved from OpenAlex<br>25 queries, 2017 to Oct 2026</div><div></div><div></div>
  <div class="down"></div><div></div><div></div>
  <div class="fb"><b>822</b>unique records after<br>de-duplication (DOI, title)</div><div></div><div></div>
  <div class="down"></div><div></div><div></div>
  <div class="fb">Screening on title, source, year,<br>citations and abstract</div><div class="right"></div>
  <div class="fb x"><b>774</b>excluded: off-scope,<br>redundant or detection-only</div>
  <div class="down"></div><div></div><div></div>
  <div class="fb f"><b>60</b>documents included<br>(48 from the search + 12 seed)<div class="chips">{chips}</div></div>
  <div class="left"></div>
  <div class="fb s"><b>12</b>seed documents<br>(earlier version<br>of this review)</div>
</div>"""

    years = list(range(2017, 2027))
    fig, ax = plt.subplots(figsize=(7.3, 5.6))
    bottom = np.zeros(len(years))
    labels = {"P": "Primary study", "R": "Review or survey", "D": "Database or resource",
              "G": "Report, perspective or governance"}
    for t in "PRDG":
        c = [sum(1 for v in CODING.values() if v[0] == y and v[1] == t) for y in years]
        ax.bar(years, c, bottom=bottom, color=TYPE_COL[t], width=0.68, label=labels[t],
               edgecolor="white", linewidth=1.2)
        bottom += np.array(c)
    for x, b in zip(years, bottom):
        if b:
            ax.text(x, b + 0.25, str(int(b)), ha="center", va="bottom", fontsize=15, fontweight="bold",
                    color=NAVY)
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) if y % 2 else str(y) for y in years], rotation=45, ha="right",
                       rotation_mode="anchor")
    ax.set_xlabel("Publication year")
    ax.set_ylabel("Number of documents")
    ax.set_ylim(0, max(bottom) + 3.5)
    ax.yaxis.grid(True, color="#E3E7EC", lw=1)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper left", fontsize=14, handlelength=1.1)
    bars = svg_of(fig)

    body = f"""<div class="grid" style="grid-template-columns: 0.95fr 1.05fr;">
{card(TEAL, "(A) Identification and selection", flow)}
{card(BLUE, "(B) Documents per year and type", bars, "display:flex;align-items:center;justify-content:center;")}
</div>"""
    render(body, "Figure_2", FLOW_CSS)


# ------------------------------------------------------------ Figure 3
def figure3():
    mat = np.zeros((len(FAMILIES), len(STEPS)), dtype=int)
    for _, _, steps, fams in CODING.values():
        for f in fams.split():
            for s in steps.split():
                mat[FAMILIES.index(f), STEPS.index(s)] += 1
    tot = [sum(1 for v in CODING.values() if f in v[3].split()) for f in FAMILIES]
    vmax = mat.max()

    import matplotlib.colors as mcolors
    cmap = mcolors.LinearSegmentedColormap.from_list("t", ["#F3F8F8", "#9CCBCB", "#1F7A80", "#0F4C52"])
    fig, (ax, axb) = plt.subplots(1, 2, figsize=(14.2, 7.2),
                                  gridspec_kw={"width_ratios": [4.4, 1.3], "wspace": 0.04})
    nR, nC = mat.shape
    for i in range(nR):
        for j in range(nC):
            v = mat[i, j]
            col = cmap(v / vmax) if v else "#F6F7F9"
            ax.add_patch(FancyBboxPatch((j + 0.06, i + 0.08), 0.88, 0.84,
                                        boxstyle="round,pad=0,rounding_size=0.12", fc=col, ec="none"))
            ax.text(j + 0.5, i + 0.5, str(v) if v else "\u2013", ha="center", va="center", fontsize=17,
                    fontweight="bold" if v else "normal",
                    color="white" if v > vmax * 0.45 else ("#1D2B3A" if v else "#A0A8B4"))
    heads = ["Hazard\nidentification", "Hazard\ncharacterization", "Exposure\nassessment",
             "Risk characterization\nand prioritization"]
    for j, (s, h) in enumerate(zip(STEPS, heads)):
        ax.add_patch(FancyBboxPatch((j + 0.04, -1.12), 0.92, 1.0, boxstyle="round,pad=0,rounding_size=0.14",
                                    fc=STEP_COL[s], ec="none"))
        ax.text(j + 0.5, -0.62, h, ha="center", va="center", color="white", fontsize=13.8, fontweight="bold",
                linespacing=1.15)
    ax.set_xlim(0, nC)
    ax.set_ylim(nR, -1.2)
    ax.set_yticks(np.arange(nR) + 0.5)
    ax.set_yticklabels([FAMILY_LABELS[f].replace("High-throughput & probabilistic", "High-throughput &\nprobabilistic")
                        .replace("QSAR, read-across & in silico", "QSAR, read-across &\nin silico")
                        for f in FAMILIES], fontsize=15)
    ax.set_xticks([])
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)

    xm = max(tot) + 7
    axb.add_patch(FancyBboxPatch((0.02 * xm, -1.12), 0.96 * xm, 1.0,
                                 boxstyle="round,pad=0,rounding_size=1.5", fc=NAVY, ec="none",
                                 mutation_aspect=0.093))
    axb.text(0.5 * xm, -0.62, "All steps\n(n = 60)", ha="center", va="center", color="white", fontsize=14.5,
             fontweight="bold", linespacing=1.15)
    yb = np.arange(nR) + 0.5
    axb.barh(yb, tot, color=NAVY, height=0.62, alpha=0.85)
    for yy, v in zip(yb, tot):
        axb.text(v + 0.7, yy, str(v), va="center", fontsize=16, fontweight="bold", color=NAVY)
    axb.set_ylim(nR, -1.2)
    axb.set_xlim(0, xm)
    axb.set_yticks([])
    axb.set_xticks([0, 10, 20, 30])
    axb.set_xlabel("Documents per family", fontsize=14)
    axb.spines["left"].set_visible(False)
    axb.spines["bottom"].set_bounds(0, 30)
    axb.spines["bottom"].set_position(("data", nR + 0.05))
    heat = svg_of(fig)

    legend = ('<div class="note" style="margin-top:6px;text-align:center">Cell value = number of documents '
              '(a document can be coded to several families and steps; cells are not additive)</div>')
    render(card(TEAL, "(A) Documents per method family and assessment step \u2002\u00b7\u2002 (B) Totals per family",
                heat + legend, "display:flex;flex-direction:column;align-items:center;"), "Figure_3")


# ------------------------------------------------------------ Figure 8
GEN_COL = {"Classical ML": GREY, "NER / transformer": BLUE, "Early LLM (GPT-3)": GOLD,
           "Recent LLM": RED, "KG-grounded LLM": GREEN}
MARK = {"Recall": "o", "Sensitivity": "o", "F1": "s", "F-score": "s", "Accuracy": "D",
        "PABAK": "^", "Precision": "v"}


def figure8():
    groups = [
        ("Literature screening", TEAL, [
            ("van den Bulk et al. (2022)", "naive Bayes + SVM, food-safety reviews", "Classical ML", [("Recall", 0.95, "")]),
            ("Bl\u00fcmmel et al. (2024)", "AI-ranked screening, threshold 0.2", "Classical ML", [("Sensitivity", 0.64, "")]),
            ("Khraisha et al. (2024)", "GPT-4, title/abstract screening", "Recent LLM", [("Accuracy", 0.67, ""), ("PABAK", 0.34, "")]),
        ]),
        ("Entity and relation extraction", BLUE, [
            ("Bl\u00fcmmel et al. (2024)", "out-of-the-box NER, test-system identity", "NER / transformer", [("F-score", 0.24, "")]),
            ("Corradi et al. (2024)", "retrained NER, compounds", "NER / transformer", [("F1", 0.88, "")]),
            ("Corradi et al. (2024)", "retrained NER, phenotypes", "NER / transformer", [("F1", 0.56, "")]),
            ("Corradi et al. (2024)", "expected liver-toxic compounds retrieved", "NER / transformer", [("Recall", 0.54, "")]),
        ]),
        ("Structured data extraction", PURPLE, [
            ("Bl\u00fcmmel et al. (2024)", "fine-tuned GPT-3 Curie, tables to OHT 201", "Early LLM (GPT-3)", [("F1", 0.2852, "")]),
            ("Khraisha et al. (2024)", "GPT-4, data extraction", "Recent LLM", [("Sensitivity", 0.75, "")]),
            ("Gartlehner et al. (2024)", "Claude 2, 160 elements from trial PDFs", "Recent LLM", [("Accuracy", 0.963, "")]),
            ("Doktorova et al. (2026)", "LLM pipeline, NOAEL and histopathology", "Recent LLM",
             [("Sensitivity", 0.95, "\u2265"), ("Precision", 0.97, "\u2265")]),
        ]),
        ("Knowledge-grounded question answering", GREEN, [
            ("An et al. (2026)", "GPT-4o alone, true/false questions", "Recent LLM", [("Accuracy", 0.62, "")]),
            ("An et al. (2026)", "knowledge graph + RAG + LLM", "KG-grounded LLM", [("Accuracy", 0.99, "")]),
        ]),
    ]
    rows = []
    y = 0
    heads = []
    for g, gc, items in groups:
        heads.append((y, g, gc))
        y += 0.9
        for it in items:
            rows.append((y, it))
            y += 1
        y += 0.25
    fig, ax = plt.subplots(figsize=(13.6, 0.5 * y + 0.9))
    for yy, g, gc in heads:
        ax.add_patch(FancyBboxPatch((-0.995, yy - 0.3), 0.96, 0.62, boxstyle="round,pad=0,rounding_size=0.08",
                                    fc=gc, ec="none", transform=ax.transData, clip_on=False))
        ax.text(-0.98, yy, "  " + g, va="center", ha="left", color="white", fontsize=15, fontweight="bold")
    for yy, (study, task, gen, vals) in rows:
        ax.text(-0.985, yy - 0.16, study, va="center", ha="left", fontsize=14.5, fontweight="bold", color=NAVY)
        ax.text(-0.985, yy + 0.22, task, va="center", ha="left", fontsize=13.5, color="#4A5565")
        ax.plot([0, 1], [yy, yy], color="#EDF0F4", lw=9, solid_capstyle="round", zorder=0)
        vmax = max(v for _, v, _ in vals)
        ax.plot([0, vmax], [yy, yy], color=GEN_COL[gen], lw=3.2, alpha=0.55, solid_capstyle="round", zorder=1)
        for k, (met, v, pre) in enumerate(sorted(vals, key=lambda t: t[1])):
            ax.scatter(v, yy, marker=MARK[met], s=150, color=GEN_COL[gen], edgecolor="white", lw=1.5, zorder=3)
            lab = f"{met} {pre}{v:.2f}"
            if len(vals) == 2 and k == 0:
                ax.annotate(lab, (v, yy), xytext=(-12, 0), textcoords="offset points", va="center", ha="right",
                            fontsize=13.5, color="#1D2B3A",
                            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
            else:
                ax.annotate(lab, (v, yy), xytext=(12, 0), textcoords="offset points", va="center", ha="left",
                            fontsize=13.5, color="#1D2B3A")
    ax.set_xlim(-1.0, 1.24)
    ax.set_ylim(y - 0.1, -0.6)
    ax.set_yticks([])
    ax.set_xticks(np.arange(0, 1.01, 0.2))
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_bounds(0, 1)
    ax.set_xlabel("Reported performance (proportion, 0\u20131)", x=0.67)
    for xv in np.arange(0, 1.01, 0.2):
        ax.axvline(xv, ymin=0, ymax=1, color="#E3E7EC", lw=1, zorder=0)
    h1 = [Line2D([], [], marker="o", ls="", color=c, markersize=12, label=g) for g, c in GEN_COL.items()]
    h2 = [Line2D([], [], marker=m, ls="", color="#5B6676", markersize=11, label=k)
          for k, m in [("Recall / sensitivity", "o"), ("F1 / F-score", "s"), ("Accuracy", "D"),
                       ("PABAK", "^"), ("Precision", "v")]]
    l1 = ax.legend(handles=h1, title="Model generation", frameon=False, loc="upper left",
                   bbox_to_anchor=(0.0, -0.075), ncol=5, title_fontproperties={"weight": "bold", "size": 14},
                   alignment="left", columnspacing=1.2, handletextpad=0.3)
    ax.add_artist(l1)
    ax.legend(handles=h2, title="Metric", frameon=False, loc="upper left", bbox_to_anchor=(0.0, -0.145),
              ncol=5, title_fontproperties={"weight": "bold", "size": 14}, alignment="left",
              columnspacing=1.2, handletextpad=0.3)
    chart = svg_of(fig)
    render(card(NAVY, "Reported performance by task", chart), "Figure_8")


# ------------------------------------------------------------ Figure 10
def figure10():
    fam = {"Classical ML": GREY, "Deep learning": PURPLE, "Transformer": TEAL}
    A = [("Logistic regression", "Classical ML", 0.802, 0.954),
         ("SVM", "Classical ML", 0.811, 0.959),
         ("LSTM", "Deep learning", None, 0.971),
         ("BiLSTM", "Deep learning", None, 0.973),
         ("BERT", "Transformer", 0.958, 0.978),
         ("RoBERTa", "Transformer", 0.962, 0.979)]
    B = [("Random forest", "Classical ML", 0.863, 0.783),
         ("XGBoost", "Classical ML", 0.895, 0.855),
         ("DistilBERT", "Transformer", 0.934, 0.904),
         ("BioBERT", "Transformer", 0.943, 0.903),
         ("BERT", "Transformer", 0.956, 0.916),
         ("RoBERTa", "Transformer", 0.962, 0.932)]

    def panel(rows, kind):
        fig, ax = plt.subplots(figsize=(5.55, 5.2))
        for i, (m, f, a, b) in enumerate(rows):
            c = fam[f]
            ax.plot([0.70, 1.0], [i, i], color="#EDF0F4", lw=10, solid_capstyle="round", zorder=0)
            if a is not None:
                ax.annotate("", xy=(b, i), xytext=(a, i),
                            arrowprops=dict(arrowstyle="-|>", color=c, lw=2.6, mutation_scale=18,
                                            shrinkA=7, shrinkB=8), zorder=2)
            if kind == "A":
                if a is not None:
                    ax.scatter(a, i, s=150, facecolor="white", edgecolor=c, lw=2.4, zorder=3)
                    ax.text(a, i - 0.34, f"{a:.3f}", ha="center", va="bottom", fontsize=13, color="#5B6676")
                ax.scatter(b, i, s=170, color=c, edgecolor="white", lw=1.5, zorder=4)
                ax.text(b + 0.008, i - 0.34, f"{b:.3f}", ha="left", va="bottom", fontsize=13,
                        color=NAVY, fontweight="bold")
            else:
                ax.scatter(a, i, s=170, marker="s", color=c, edgecolor="white", lw=1.5, zorder=4)
                ax.scatter(b, i, s=180, marker="D", facecolor="white", edgecolor=c, lw=2.4, zorder=3)
                ax.text(a + 0.006, i - 0.34, f"{a:.3f}", ha="left", va="bottom", fontsize=13,
                        color=NAVY, fontweight="bold")
                ax.text(b, i - 0.34, f"{b:.3f}", ha="center", va="bottom", fontsize=13, color="#5B6676")
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels([r[0] for r in rows], fontsize=15)
        for t, r in zip(ax.get_yticklabels(), rows):
            t.set_color(fam[r[1]])
            t.set_fontweight("bold")
        ax.set_ylim(len(rows) - 0.5, -0.9)
        ax.set_xlim(0.70, 1.0)
        ax.set_xticks([0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00])
        ax.set_xlabel("Accuracy on the held-out test set")
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
        ax.xaxis.grid(True, color="#E3E7EC", lw=1)
        ax.set_axisbelow(True)
        if kind == "A":
            h = [Line2D([], [], marker="o", ls="", markerfacecolor="white", markeredgecolor="#5B6676",
                        markeredgewidth=2, markersize=11, label="Original data"),
                 Line2D([], [], marker="o", ls="", color="#5B6676", markersize=11, label="After data enrichment")]
        else:
            h = [Line2D([], [], marker="s", ls="", color="#5B6676", markersize=11, label="Binary task"),
                 Line2D([], [], marker="D", ls="", markerfacecolor="white", markeredgecolor="#5B6676",
                        markeredgewidth=2, markersize=11, label="Multi-class task")]
        ax.legend(handles=h, frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2,
                  fontsize=14, handletextpad=0.3, columnspacing=1.4)
        return svg_of(fig)

    keys = "".join(f'<span style="display:inline-flex;align-items:center;margin:0 14px">'
                   f'<span style="width:16px;height:16px;border-radius:50%;background:{c};margin-right:7px"></span>{f}</span>'
                   for f, c in fam.items())
    body = f"""<div class="grid" style="grid-template-columns: 1fr 1fr;">
{card(TEAL, "(A) Effect of data enrichment (Sari et al., 2025a)", panel(A, "A"), "display:flex;justify-content:center;")}
{card(BLUE, "(B) Binary vs multi-class task (Sari et al., 2025b)", panel(B, "B"), "display:flex;justify-content:center;")}
</div><div class="note" style="text-align:center;margin-top:12px;font-size:18px">{keys}
<span style="margin-left:18px">LSTM and BiLSTM: original-data accuracy not reported</span></div>"""
    render(body, "Figure_10")


# ------------------------------------------------------------ Figure 11
def figure11():
    rows = [
        ("Wang et al. (2023)", "Bayesian network, heavy metals in feed (0.65% positives)",
         "overall accuracy vs accuracy on contaminated batches", 0.9936, 0.2029),
        ("Castano-Duque et al. (2022)", "gradient boosting, aflatoxin in maize (4% > 20 ppb)",
         "overall accuracy vs high-contamination class", 0.94, 0.61),
        ("Castano-Duque et al. (2022)", "Bayesian network, aflatoxin in maize",
         "overall accuracy vs high-contamination class", 0.94, 0.71),
        ("Castano-Duque et al. (2022)", "gradient boosting, fumonisin, 2021 validation year",
         "overall accuracy vs balanced accuracy, high class", 0.97, 0.55),
        ("Khraisha et al. (2024)", "GPT-4, title/abstract screening",
         "accuracy vs PABAK (chance-adjusted agreement)", 0.67, 0.34),
        ("Khraisha et al. (2024)", "GPT-4, full-text screening",
         "accuracy vs Cohen's kappa", 0.69, 0.07),
        ("Zhang et al. (2026b)", "knowledge-graph recall-risk model, temporal hold-out",
         "ROC AUC vs average precision", 0.8227, 0.4107),
    ]
    fig, ax = plt.subplots(figsize=(13.6, 8.2))
    for i, (st, mod, met, h, a) in enumerate(rows):
        ax.text(-1.06, i - 0.25, st, fontsize=15, fontweight="bold", color=NAVY, va="center")
        ax.text(-1.06, i + 0.05, mod, fontsize=13.5, color="#3A4656", va="center")
        ax.text(-1.06, i + 0.33, met, fontsize=13, color="#7A8494", va="center", style="italic")
        ax.plot([0, 1], [i, i], color="#EDF0F4", lw=12, solid_capstyle="round", zorder=0)
        ax.plot([a, h], [i, i], color="#E8A39B", lw=5, solid_capstyle="round", zorder=1)
        ax.scatter(h, i, s=190, color=NAVY, edgecolor="white", lw=1.5, zorder=3)
        ax.scatter(a, i, s=200, marker="D", color=RED, edgecolor="white", lw=1.5, zorder=3)
        ax.text(h + 0.022, i, f"{h:.2f}", va="center", ha="left", fontsize=14, color=NAVY, fontweight="bold")
        ax.text(a - 0.022, i, f"{a:.2f}", va="center", ha="right", fontsize=14, color=RED, fontweight="bold")
        ax.text(1.215, i, f"\u2212{h - a:.2f}", va="center", ha="center", fontsize=15, color=RED,
                fontweight="bold", bbox=dict(boxstyle="round,pad=0.3", fc=TINT[RED], ec="none"))
    ax.text(1.215, -0.85, "gap", ha="center", fontsize=14, color="#5B6676", fontweight="bold")
    ax.set_xlim(-1.08, 1.28)
    ax.set_ylim(len(rows) - 0.4, -1.0)
    ax.set_yticks([])
    ax.set_xticks(np.arange(0, 1.01, 0.2))
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_bounds(0, 1)
    ax.set_xlabel("Reported value (proportion, 0\u20131)", x=0.6)
    for xv in np.arange(0, 1.01, 0.2):
        ax.axvline(xv, color="#E3E7EC", lw=1, zorder=0)
    h = [Line2D([], [], marker="o", ls="", color=NAVY, markersize=12, label="Headline metric"),
         Line2D([], [], marker="D", ls="", color=RED, markersize=11,
                label="Minority-class or chance-adjusted metric (same study, same data)")]
    ax.legend(handles=h, frameon=False, loc="lower left", bbox_to_anchor=(0.46, 1.0), ncol=1, fontsize=14)
    render(card(RED, "Headline accuracy can hide poor detection of the class that matters", svg_of(fig)),
           "Figure_11")


# ------------------------------------------------------------ Figure 14
MAT_CSS = """
table.m { border-collapse: separate; border-spacing: 6px 6px; width: 100%; font-size: 18px; }
table.m th { font-size: 17px; font-weight: 600; color: #fff; background: #1D3557; border-radius: 9px;
             padding: 8px 6px; line-height: 1.2; }
table.m th.app { background: none; color: #1D3557; text-align: left; font-size: 18px; }
table.m td.app { text-align: left; padding: 6px 10px 6px 12px; border-radius: 9px; font-weight: 600;
                 line-height: 1.2; color: #1D2B3A; }
table.m td.lv { border-radius: 9px; text-align: center; padding: 6px 4px; font-size: 16.5px; font-weight: 600; }
.dots { letter-spacing: 3px; font-size: 15px; display: block; line-height: 1; margin-bottom: 2px; }
.lv3 { background: #E3F1DF; color: #2F6B27; } .lv2 { background: #FBF0D9; color: #8A5A0B; }
.lv1 { background: #F8E1DE; color: #9B2C20; }
.step { display: inline-block; font-size: 13.5px; font-weight: 700; color: #fff; border-radius: 6px;
        padding: 1px 7px; margin-right: 8px; vertical-align: 2px; }
.leg { display: flex; gap: 22px; justify-content: center; margin-top: 10px; font-size: 17px; }
.leg span.b { display: inline-block; padding: 3px 12px; border-radius: 7px; font-weight: 600; }
"""


def figure14():
    apps = [
        ("HI", "Literature search and screening prioritization", [3, 2, 2, 2, 3]),
        ("HI", "LLM data extraction from literature and reports", [3, 1, 2, 1, 2]),
        ("HI", "Ontology mapping and knowledge graphs", [2, 1, 3, 2, 1]),
        ("HC", "Curated toxicological databases", [3, 2, 3, 3, 3]),
        ("HC", "QSAR, read-across and ML hazard prediction", [3, 2, 2, 2, 2]),
        ("HC", "LLM-assisted derivation of PoDs or HBGVs", [1, 1, 1, 1, 1]),
        ("EA", "High-throughput exposure modelling", [2, 2, 2, 2, 2]),
        ("EA", "ML prediction of contaminant occurrence", [3, 3, 2, 3, 2]),
        ("RC", "Classification of alert and recall text", [2, 2, 1, 2, 1]),
        ("RC", "Integrated risk ranking and early warning", [2, 2, 2, 2, 1]),
    ]
    cols = ["Volume of<br>evidence", "External or temporal<br>validation", "Explainability<br>and provenance",
            "Food-chemical<br>specificity", "Regulatory<br>readiness"]
    lab = {3: "Strong", 2: "Moderate", 1: "Limited"}
    dots = {3: "\u25cf\u25cf\u25cf", 2: "\u25cf\u25cf\u25cb", 1: "\u25cf\u25cb\u25cb"}
    stepname = {"HI": "HI", "HC": "HC", "EA": "EA", "RC": "RC"}
    trs = []
    for s, a, sc in apps:
        cells = "".join(f'<td class="lv lv{v}"><span class="dots">{dots[v]}</span>{lab[v]}</td>' for v in sc)
        trs.append(f'<tr><td class="app" style="background:{TINT[STEP_COL[s]]}">'
                   f'<span class="step" style="background:{STEP_COL[s]}">{stepname[s]}</span>{a}</td>{cells}</tr>')
    head = '<tr><th class="app">Application area</th>' + "".join(f"<th>{c}</th>" for c in cols) + "</tr>"
    steps = "".join(f'<span><span class="b" style="background:{STEP_COL[k]};color:#fff">{k}</span> {v}</span>'
                    for k, v in [("HI", "hazard identification"), ("HC", "hazard characterization"),
                                 ("EA", "exposure assessment"), ("RC", "risk characterization & prioritization")])
    table = f'<table class="m"><colgroup><col style="width:36%"></colgroup>{head}{"".join(trs)}</table>' \
            f'<div class="leg">{steps}</div>'
    render(card(NAVY, "Maturity of AI application areas", table), "Figure_14", MAT_CSS)


# ------------------------------------------------------------ Figure 15
FW_CSS = """
.fw { display: grid; grid-template-columns: 1fr 46px; column-gap: 8px; }
.layer { position: relative; border-radius: 16px; padding: 38px 16px 14px; margin-bottom: 30px;
         border: 2.5px solid var(--c); background: var(--t); }
.layer > .tag { left: 22px; transform: translate(0, -50%); }
.row { display: flex; gap: 10px; align-items: stretch; }
.bx { flex: 1; background: #fff; border-radius: 11px; border: 1.5px solid var(--c); padding: 9px 9px;
      text-align: center; font-size: 15.5px; line-height: 1.28; position: relative; }
.bx b { display: block; font-size: 17px; color: var(--c); margin-bottom: 3px; line-height: 1.2; }
.bx i { color: #4A5565; }
.ar { flex: 0 0 18px; display: flex; align-items: center; justify-content: center; }
.ar::after { content: ''; border: 9px solid transparent; border-left: 12px solid #5B6676; border-right: 0; }
.dn { position: absolute; left: 50%; bottom: -30px; transform: translateX(-50%); width: 0; height: 30px; }
.dn::before { content: ''; position: absolute; left: -1.5px; top: 2px; bottom: 10px; border-left: 3px solid #5B6676; }
.dn::after { content: ''; position: absolute; left: -9px; bottom: 0; border: 9px solid transparent;
             border-top: 12px solid #5B6676; border-bottom: 0; }
.dnlab { position: absolute; left: calc(50% + 16px); bottom: -27px; font-size: 15px; color: #4A5565; font-style: italic; }
.badge { position: absolute; top: -14px; right: -10px; width: 34px; height: 34px; border-radius: 50%;
         background: #6B4FA0; color: #fff; font-size: 14.5px; font-weight: 700; display: flex;
         align-items: center; justify-content: center; border: 2.5px solid #fff; box-shadow: 0 0 0 1px #6B4FA0; }
.eq { display: inline-block; font-family: 'Cambria Math', 'Segoe UI'; font-size: 15.5px; background: #F6F7F9;
      border-radius: 6px; padding: 1px 6px; margin-top: 4px; color: #1D2B3A; }
.gov { border: 2px dashed #6B4FA0; background: #fff; border-radius: 11px; padding: 9px 14px; font-size: 15.5px;
       line-height: 1.35; margin-top: 12px; }
.gov b { color: #6B4FA0; }
.lane { position: relative; }
.lane .ln { position: absolute; left: 50%; top: 80px; bottom: 58px; border-left: 3px dashed #6B4FA0; }
.lane .h1 { position: absolute; left: -6px; width: calc(50% + 7px); top: 80px; border-top: 3px dashed #6B4FA0; }
.lane .h1::before { content: ''; position: absolute; left: -4px; top: -10.5px; border: 9px solid transparent;
                    border-right: 12px solid #6B4FA0; border-left: 0; }
.lane .h4 { position: absolute; left: -8px; width: calc(50% + 9px); bottom: 58px; border-top: 3px dashed #6B4FA0; }
.eq { white-space: nowrap; }
.lane .tx { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%) rotate(-90deg);
            white-space: nowrap; font-size: 16px; color: #6B4FA0; font-weight: 600; background: #fff; padding: 0 8px; }
.lane .hz { position: absolute; left: -8px; right: 50%; border-top: 3px dashed #6B4FA0; }
"""


def figure15():
    def L(color, tag, inner, extra=""):
        return (f'<div class="layer" style="--c:{color};--t:{TINT[color]};{extra}"><div class="tag" '
                f'style="--c:{color}">{tag}</div>{inner}</div>')

    def bx(title, txt, badge="", c=None, style=""):
        cs = f"--c:{c};" if c else ""
        b = f'<div class="badge">{badge}</div>' if badge else ""
        return f'<div class="bx" style="{cs}{style}">{b}<b>{title}</b>{txt}</div>'

    ar = '<div class="ar"></div>'
    src = "".join([
        bx("Scientific literature", "MEDLINE, Embase,<br>Web of Science,<br>grey literature"),
        bx("Regulatory opinions", "EFSA, JECFA,<br>Health Canada, FDA"),
        bx("Alerts and recalls", "RASFF, CFIA,<br>FDA recalls"),
        bx("Occurrence data", "monitoring and<br>surveillance programmes"),
        bx("Food consumption", "national dietary<br>surveys, GEMS/Food"),
        bx("Curated databases", "OpenFoodTox, CompTox,<br>FRAC-TD, T3DB"),
    ])
    l1 = L(BLUE, "1 \u2002Evidence sources", f'<div class="row">{src}</div><div class="dn"></div>')

    ai = ar.join([
        bx("Retrieval and screening", "ML or LLM ranking;<br>95% recall stopping rule", "H1"),
        bx("Schema-constrained extraction", "LLM / NER to OECD OHT fields;<br>answers grounded in<br>verbatim quotations", "H2"),
        bx("Normalization", "FoodOn, FoodEx2, ChEBI,<br>CAS / DTXSID, units"),
        bx("Knowledge graph", "chemical \u2013 food \u2013 effect \u2013<br>value \u2013 source triples<br>with provenance"),
    ])
    l2 = L(GOLD, "2 \u2002AI evidence layer", f'<div class="row">{ai}</div>'
           f'<div class="dn"></div><div class="dnlab">structured, versioned evidence</div>')

    eng = ar.join([
        bx("Hazard identification", "evidence maps; automated<br>systematic review; alert-text<br>classifiers; emerging signals", c=TEAL),
        bx("Hazard characterization", "NOAEL / LOAEL / BMDL<br>\u2192 ADI / TDI; QSAR or<br>read-across within domain;<br>TTC fallback", "H3", c=BLUE),
        bx("Exposure assessment", "ML occurrence models;<br>Monte Carlo simulation<br><span class='eq'>EDI = \u03a3 (C \u00d7 F) / bw</span><br>"
           "<i>C, concentration; F, food intake</i>", c=GREEN),
        bx("Risk characterization", "<span class='eq'>HQ = EDI / HBGV</span><br><i>threshold effects</i><br>"
           "<span class='eq'>MOE = BMDL / EDI</span><br><i>genotoxic carcinogens</i>", c=GOLD),
        bx("Prioritization", "multi-criteria ranking<br>with uncertainty bounds,<br>evidence strength and<br>data-gap flags", "H4", c=RED),
    ])
    gov = ('<div class="gov"><b>Cross-cutting governance</b> \u2014 human checkpoints H1\u2013H4 (screening audit, '
           'extraction verification, selection of PoD/HBGV, ranking sign-off); explainability (SHAP, links to source '
           'sentences); logging of model, version, prompt and date; readiness criteria (OECD QAF, ReadyAI); '
           'EU AI Act and agency policies</div>')
    l3 = L(GREEN, "3 \u2002Risk assessment and prioritization engine", f'<div class="row">{eng}</div>{gov}'
           f'<div class="dn"></div>')

    outs = "".join([
        bx("Ranked chemical\u2013food pairs", "with HQ / MOE, uncertainty<br>and evidence strength", c=PURPLE),
        bx("Evidence dossier", "every value traceable to<br>source sentences and tables", c=PURPLE),
        bx("Data-gap map", "targets for monitoring,<br>testing and new reviews", c=PURPLE),
        bx("Risk managers and assessors", "decisions, full assessments<br>and feedback", c=NAVY,
           style="border-width:2.5px;background:#F4F6FA"),
    ])
    l4 = L(PURPLE, "4 \u2002Outputs and decisions", f'<div class="row">{outs}</div>', "margin-bottom:0")

    lane = ('<div class="lane"><div class="ln"></div><div class="h1"></div><div class="h4"></div>'
            '<div class="tx">feedback: re-prioritization and model updating</div></div>')
    body = f'<div class="fw"><div>{l1}{l2}{l3}{l4}</div>{lane}</div>'
    render(body, "Figure_15", FW_CSS)


if __name__ == "__main__":
    todo = sys.argv[1:] or ["2", "3", "8", "10", "11", "14", "15"]
    funcs = {"2": figure2, "3": figure3, "8": figure8, "10": figure10,
             "11": figure11, "14": figure14, "15": figure15}
    for t in todo:
        funcs[t]()
