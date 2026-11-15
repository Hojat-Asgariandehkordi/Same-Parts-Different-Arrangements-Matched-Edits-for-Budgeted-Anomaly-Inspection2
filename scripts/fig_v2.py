"""Data figures of the paper, drawn only from the code export in data/ (results_export/figure_data).

spread.pdf          one column: (a) untouched compartments that change vs change cutoff (collateral.csv),
                    (b) untouched same-class instances after one extra instance (insertion_same_class.csv)
native_results.pdf  one column: (a) sPRO curves on real pushpin defects (native_results_curves.csv),
                    (b) defective compartments found vs intact compartments opened (native_results_points.csv)
Colours: released grey, class-wide purple, footprint green, released top-3 list black square;
seed 1 filled / solid, seed 2 hollow / dashed. Intervals are the 95% bootstrap intervals of the export.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style  # noqa: E402

style.setup()
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

C = style.C
DATA = Path(__file__).resolve().parent.parent / "data"
LIST = "#111111"


def spread():
    col = pd.read_csv(DATA / "collateral.csv")
    ins = pd.read_csv(DATA / "insertion_same_class.csv")
    fig, (a, b) = plt.subplots(1, 2, figsize=(style.COL, 2.2), gridspec_kw=dict(width_ratios=[1.15, 1], wspace=.5))
    fig.subplots_adjust(bottom=.37, top=.93)
    curves = [("released", "fault", C["released"], "-", "released, relocation"),
              ("released", "vacancy", C["vacancy"], "-", "released, vacancy only"),
              ("released", "sham", C["sham"], "-", "released, valid sham"),
              ("scr_cw_s2", "fault", C["classwide"], "-", "class-wide, relocation"),
              ("scr_fp_s1", "fault", C["footprint"], "-", "footprint, relocation"),
              ("scr_fp_s2", "fault", C["footprint"], "--", None)]
    for head, edit, color, ls, lab in curves:
        d = col[(col["head"] == head) & (col.interface == "extracted") & (col.edit == edit)].sort_values("cutoff")
        a.fill_between(d.cutoff, 100 * d.ci_low, 100 * d.ci_high, color=color, alpha=.2, lw=0)
        a.plot(d.cutoff, 100 * d.share, color=color, ls=ls, lw=1.2, label=lab)
    a.axvline(.5, color=C["grey"], lw=.6, ls=":")
    a.set_xlim(0, 1), a.set_ylim(0, 102)
    a.set_xlabel("change cutoff")
    a.set_ylabel("untouched compartments (%)")
    style.panel(a, "a", x=-.28)
    a.text(.52, 50, "0.5", fontsize=7, color=C["grey"])
    # (b) insertion probe, 800-step continuation heads (ft*)
    ft = ins[ins.file == "summary_ft.csv"]
    cats = [("pushpins", "pushpins"), ("screw_bag", "screw bag")]
    wd = .26
    for i, (cat, name) in enumerate(cats):
        r = ft[(ft.category == cat) & (ft["head"] == "released")].iloc[0]
        b.bar(i - wd, 100 * r.same_any, wd, color=C["released"], alpha=.85, lw=0)
        b.errorbar(i - wd, 100 * r.same_any, yerr=[[100 * (r.same_any - r.same_any_lo)], [100 * (r.same_any_hi - r.same_any)]],
                   fmt="none", ecolor="k", elinewidth=.8, capsize=2)
        for j, arm in enumerate(("classwide", "footprint")):
            rows = [ft[(ft.category == cat) & (ft["head"] == f"ft{s}_{arm}")].iloc[0] for s in (3407, 3419)]
            x = i + j * wd
            b.bar(x, 100 * np.mean([r.same_any for r in rows]), wd, color=C[arm], alpha=.85, lw=0)
            for k, r in enumerate(rows):
                y = 100 * r.same_any
                b.errorbar(x + (k - .5) * wd * .4, y, yerr=[[y - 100 * r.same_any_lo], [100 * r.same_any_hi - y]],
                           fmt="o", color="k", ms=2.6, mfc="white" if k else "k", elinewidth=.8, capsize=1.5)
    b.set_xticks(range(2), [c[1] for c in cats])
    b.set_ylim(0, 105)
    b.set_ylabel("same-class instances (%)")
    b.grid(axis="x", visible=False)
    h = [Line2D([], [], color=c, lw=1.4, ls=ls) for c, ls in ((C["released"], "-"), (C["vacancy"], "-"), (C["sham"], "-"),
                                                             (C["classwide"], "-"), (C["footprint"], "-"), (C["footprint"], "--"))]
    fig.legend(h, ["released: relocation", "released: vacancy only", "released: valid sham",
                   "class-wide: relocation", "footprint: relocation, seed 1", "footprint: relocation, seed 2"],
               loc="lower center", ncol=2, fontsize=7, frameon=False, handlelength=1.6, columnspacing=1.0,
               labelspacing=.25, bbox_to_anchor=(.5, -.01))
    style.panel(b, "b", x=-.3)
    style.save(fig, "spread")


def native_results():
    cur = pd.read_csv(DATA / "native_results_curves.csv")
    pts = pd.read_csv(DATA / "native_results_points.csv")
    fig, (a, b) = plt.subplots(1, 2, figsize=(style.COL, 2.3), gridspec_kw=dict(wspace=.48))
    fig.subplots_adjust(bottom=.36, top=.93)
    for head, color, ls in (("released", C["released"], "-"), ("ft3407_classwide", C["classwide"], "-"),
                            ("ft3419_classwide", C["classwide"], "--"), ("ft3407_footprint", C["footprint"], "-"),
                            ("ft3419_footprint", C["footprint"], "--")):
        d = cur[cur["head"] == head]
        a.plot(100 * d.fpr, 100 * d.spro, color=color, ls=ls, lw=1.2)
    a.set_xlim(0, 5), a.set_ylim(0, 100)
    a.set_xlabel("false-positive rate (%)")
    a.set_ylabel("sPRO (%)")
    style.panel(a, "a", x=-.26)

    def get(f, head, pol):
        d = pts[(pts.file == f) & (pts["head"] == head) & (pts.subset == pol)].set_index("metric")
        return d.loc["recall"], d.loc["waste_per_anomaly"]

    marks = [("pushpins_summary.csv", "released", "threshold", C["released"], "o", False, 4.5),
             ("pushpins_summary.csv", "released", "list", LIST, "s", False, 4.5)]
    for k, s in enumerate((3407, 3419)):
        marks += [("pushpins_summary.csv", f"ft{s}_footprint", "threshold", C["footprint"], "o", k == 1, 4),
                  (f"pushpins_scratch{s}_summary.csv", f"scr{s}_classwide", "threshold", C["classwide"], "*", k == 1, 7),
                  (f"pushpins_scratch{s}_summary.csv", f"scr{s}_footprint", "threshold", C["footprint"], "*", k == 1, 7)]
    for f, head, pol, color, m, hollow, ms in marks:
        r, w = get(f, head, pol)
        b.errorbar(w["mean"], 100 * r["mean"], xerr=[[w["mean"] - w.lo], [w.hi - w["mean"]]],
                   yerr=[[100 * (r["mean"] - r.lo)], [100 * (r.hi - r["mean"])]], fmt=m, color=color, ms=ms,
                   mfc="white" if hollow else color, mew=.9, elinewidth=.8, capsize=1.5, zorder=4)
    b.set_xlim(-.3, 7.3), b.set_ylim(30, 100)
    b.set_xlabel("intact opened per tray")
    b.set_ylabel("defective found (%)")
    prox = [Line2D([], [], marker="o", color=C["released"], ms=4), Line2D([], [], marker="s", ls="", color=LIST, ms=4),
            Line2D([], [], marker="o", color=C["classwide"], ms=4), Line2D([], [], marker="o", color=C["footprint"], ms=4),
            Line2D([], [], marker="*", ls="", color=C["footprint"], ms=7), Line2D([], [], marker="*", ls="", color=C["classwide"], ms=7)]
    fig.legend(prox, ["released (a); threshold (b)", "released, top-3 list (b)", "class-wide, 1.6k steps (a)",
                      "footprint, 1.6k steps", "footprint, from scratch (b)", "class-wide, from scratch (b)"],
               loc="lower center", ncol=2, fontsize=7, frameon=False, handletextpad=.3, columnspacing=.8,
               labelspacing=.25, handlelength=1.4, bbox_to_anchor=(.5, -.01))
    style.panel(b, "b", x=-.3)
    style.save(fig, "native_results")


def collateral():
    """Supplement: released head, both input paths, three edits (collateral.csv)."""
    col = pd.read_csv(DATA / "collateral.csv")
    fig, axes = plt.subplots(1, 2, figsize=(style.FULL * .75, 1.9), sharey=True, gridspec_kw=dict(wspace=.12))
    fig.subplots_adjust(bottom=.24, top=.88, right=.73)
    for ax, (itf, name) in zip(axes, (("oracle", "oracle part maps"), ("extracted", "re-segmented part maps"))):
        for edit, color, lab in (("fault", C["fault"], "relocation (fault)"), ("vacancy", C["vacancy"], "vacancy only"),
                                 ("sham", C["sham"], "valid sham")):
            d = col[(col["head"] == "released") & (col.interface == itf) & (col.edit == edit)].sort_values("cutoff")
            ax.fill_between(d.cutoff, 100 * d.ci_low, 100 * d.ci_high, color=color, alpha=.2, lw=0)
            ax.plot(d.cutoff, 100 * d.share, color=color, lw=1.3, label=lab)
        ax.axvline(.5, color=C["grey"], lw=.6, ls=":")
        ax.set_xlim(0, 1), ax.set_ylim(0, 102)
        ax.set_xticks([0, .5, 1])
        ax.set_xlabel("change cutoff")
        ax.set_title(name, fontsize=8, pad=3)
    axes[0].set_ylabel("untouched compartments (%)")
    axes[1].legend(loc="center left", bbox_to_anchor=(1.03, .5), fontsize=7.5, frameon=False)
    style.save(fig, "collateral")


if __name__ == "__main__":
    spread()
    native_results()
