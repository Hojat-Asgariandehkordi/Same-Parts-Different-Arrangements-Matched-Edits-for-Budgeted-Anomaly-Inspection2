#!/usr/bin/env bash
# Rebuild every figure and both PDFs.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -I scripts/recover_vector.py figures/orig
python3 -I scripts/fig_schematic.py
python3 -I scripts/fig_results.py
python3 -I scripts/fig_supplement.py
python3 -I scripts/fig_v2.py          # spread.pdf, native_results.pdf from data/ (v2 results export)
latexmk -pdf -interaction=nonstopmode main.tex   # main paper + supplementary material in one PDF
