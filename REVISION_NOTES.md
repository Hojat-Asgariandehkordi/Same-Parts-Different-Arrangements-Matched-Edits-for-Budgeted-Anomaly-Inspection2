# Paper 4, version 2: revision notes

This repository holds the second version of *Same Parts, Different Arrangements: Matched Edits for Budgeted Anomaly Inspection*.
The science and every number come from the v2 manuscript received from the server (baseline commit `a0745d8`) and from
`results_export` (Cursor export). Structure, notation, writing conventions, figure style and BioRender art come from the first
version (repo `...-Inspection`, commit `5a5ebeb`), which is unchanged.

## Main paper (8 pages + references, CVPR 2027 kit)
- Title kept from version 1. Abstract in plain language with one message; toy example before the contributions;
  connected contributions ("First, ... Second, ..."); related work in two paragraphs.
- Notation of version 1: scene cutoff `t_s`, compartment cutoff `t_c`, cost `C` (v2 used tau, t, W); Alg. 1 kept.
  Insertion targets `y^cw`, `y^fp`; part label `l(p)` (no clash with the loss `ell`). Spread is defined in Sec. 4 before use.
- Lead result: from-scratch footprint heads vs the released top-3 list on real pushpin defects (`\scrVsListR`, `\scrVsListW`),
  with the pooled development rule throughout. The dev-faults-only rule is a robustness paragraph in the supplement.
- Caveats stated in the text: sham alarms 36/35 vs 10/12 sources; seed-1 class-wide arm fails the reproduction check;
  1.6k-step continuations do not beat the released list on cost and lower pushpin image AUROC; two seeds.
- Words removed: "registered", "pinned", "earlier rounds". Fixed macros `\sixFP`/`\sixCW` (en-dash ranges).
- Table of SALAD's full system and the real-defect example figure moved to the supplement (page limit).
- LLM statement on page 8 (checked with pdftotext).

## Figures (Times / STIX, >= 7 pt, one meaning per colour)
- Fig. 1 teaser: BioRender matched trays + footprint/class-wide schematic (version 1).
- Fig. 2 pipeline: version 1 layout, test photo 058 from the export, compartment edges from `data/compartment_grid.csv`.
- Fig. 3 native_results and Fig. 4 spread: rebuilt from `data/*.csv` by `scripts/fig_results.py` (one column each).
- Supplement: `collateral.pdf` rebuilt from `data/collateral.csv`; `native_examples.pdf` re-rendered from v2's SVG with
  TeX Gyre Termes and our palette (its maps keep v2's heat colour map because only the rendered rasters exist).

## Supplement
- "Part A / Part B: record of earlier rounds" framing removed. Sections: order of analyses, inspection definitions,
  continuations, native AU-sPRO, real defects at fixed operating points (+ dev-only robustness), from-scratch recipe,
  insertion probe, appearance detectors, full SALAD, edit construction, 800-step fine-tunes, full fusion and juice rule.
- Dropped from the build (still in git history): graph audit, medical data-use note, clinical query, v3 decision rules.

## Open points for the group
- Dev-only robustness numbers use the export's bootstrap seed 0 (paper intervals use seeds 2026/2027).
- `\scratchSentence` (`[pending]`) is unused; `\scratchEndpoints` reports the failed seed-1 reproduction check honestly.
- The repository is public; consider making it private before submission.

## Template: identical to the CVPR 2027 author kit (v1)
- `cvpr.sty` and `ieeenat_fullname.bst` are byte-identical to the kit.
- `preamble.tex` is the kit file unchanged (microtype stays commented out, as in the kit); this paper's packages and
  macros are appended at its end, where the kit says to import them.
- `main.tex` is the kit's `main.tex` with only the title, author and `\input{sec/...}` lines changed; the text lives in
  `sec/0_abstract.tex` ... `sec/6_llm_statement.tex`, and the bibliography is `main.bib`, as in the kit.
- The supplement is the kit's `sec/X_suppl.tex` (`\clearpage`, `\setcounter{page}{1}`, `\maketitlesupplementary`),
  included at the end of `main.tex` exactly where the kit places it, so `main.pdf` holds the paper and the supplementary
  material in one file (31 pages: paper pp. 1-8, references pp. 9-10, supplement from p. 11 with its own page numbers).
  The separate `supplement.tex` was removed; the duplicate LLM statement in the supplement was dropped. Main-text
  pointers to the supplement are now live cross-references.
- Before submission, split the PDF at the supplement if CVPR asks for separate files (the kit's warning in `main.tex`).
- With microtype off the main text and LLM statement still end on page 8; references start on page 9.
