#!/bin/sh
# Rebuild every figure and both PDFs. Data figures read only data/ (copied from results_export/figure_data).
set -e
cd "$(dirname "$0")/.."
python3 scripts/fig_schematic.py      # Fig. 1 (teaser) and Fig. 2 (pipeline)
python3 scripts/fig_results.py        # spread, native_results, supplementary collateral
latexmk -pdf main.tex
latexmk -pdf supplement.tex
