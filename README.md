# Figures for *Artificial intelligence for food chemical risk assessment and prioritization*

Code that reproduces Figures 2, 3, 8, 10, 11, 14 and 15 of the review submitted to *Frontiers in Toxicology*.

Figures 2 and 3 are drawn from the coded corpus of 60 documents in `corpus_coding.py`. Figures 8, 10 and 11 plot values reported in the cited studies. Figures 14 and 15 are diagrams. The values are those used in the manuscript; this repository does not re-extract them from the source papers.

## Requirements

Python 3.10 or later, on Windows with Microsoft Edge installed (figures are rendered through Edge via Playwright, using Segoe UI):

```
pip install -r requirements.txt
python -m playwright install
```

## Run

```
python make_figures_v2.py
```

PNG and TIFF files are written to `figures/` at 600 dpi. To draw a subset:

```
python make_figures_v2.py 2 3 8
```

## Licence

MIT. See `LICENSE`.
