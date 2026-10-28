"""
UK high street turnaround: the analysis behind the case.

Reads the public-data snapshots in data/, prints the key numbers used in the case write-up,
and saves the charts used in the README and the deck to charts/.

    pip install -r requirements.txt
    python high_street_analysis.py

Every chart title states the finding (an "action title"), not just the topic.
"""
from pathlib import Path

import matplotlib
import matplotlib.ticker
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

import os
HERE = Path(__file__).parent
DATA = HERE / "data"
# PLAIN=1 saves untitled versions (for slides, where the slide title carries the message).
PLAIN = os.environ.get("PLAIN") == "1"
OUT = HERE / "charts" / ("plain" if PLAIN else "")
OUT.mkdir(parents=True, exist_ok=True)

# Validated categorical palette (slots 1-3 pass colour-blind checks as a set) and neutral ink.
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK_2, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1", "#fcfcfb"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": GRID,
    "axes.labelcolor": INK_2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.grid": True,
    "axes.grid.axis": "y",
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "xtick.color": INK_2,
    "ytick.color": INK_2,
    "xtick.major.size": 0,
    "ytick.major.size": 0,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "legend.frameon": False,
})


def titled(ax, title, subtitle):
    if PLAIN:
        ax.text(0, 1.03, subtitle, transform=ax.transAxes, fontsize=12, color=INK_2, va="bottom")
        return
    ax.set_title(title, loc="left", fontsize=15, fontweight="bold", color=INK, pad=30)
    ax.text(0, 1.03, subtitle, transform=ax.transAxes, fontsize=10.5, color=INK_2, va="bottom")


def source(fig, text):
    if PLAIN:
        return
    fig.text(0.012, -0.02, "Source: " + text, fontsize=8.5, color=MUTED, ha="left", va="top")


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print(f"  saved charts/{name}")


# ---------------------------------------------------------------- 1. Demand has moved online
online = pd.read_csv(DATA / "online_share.csv")
o = online.set_index("year")["online_share_pct"]
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(o.index, o.values, color=BLUE, linewidth=2.2, marker="o", markersize=6,
        markeredgecolor=SURFACE, markeredgewidth=1.5, zorder=3)
ax.axvspan(2019.6, 2021.4, color="#f1f0ec", zorder=0)
ax.text(2020.5, 3.0, "Pandemic", ha="center", fontsize=9.5, color=MUTED)
for yr in (2007, 2019, 2021, 2025):
    ax.annotate(f"{o[yr]:.1f}%", (yr, o[yr]), textcoords="offset points",
                xytext=(0, 10), ha="center", fontsize=10, color=INK, fontweight="bold")
ax.set_ylim(0, 36)
ax.set_xlim(2006, 2026)
ax.set_xticks([2007, 2010, 2013, 2016, 2019, 2022, 2025])
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
titled(ax, "More than a quarter of retail spending is now online, and it has not come back",
       "Internet sales as % of total UK retail sales, annual average")
source(fig, "ONS Retail Sales Index, series J4MC (years shown are those published in the source snapshot)")
save(fig, "01_online_share.png")

# ---------------------------------------------------------------- 2. Who is closing
cl = pd.read_csv(DATA / "store_closures.csv")
actual = cl[cl.status == "actual"]
fig, ax = plt.subplots(figsize=(9, 5))
x = actual.year
ax.bar(x, actual.independent_closures, color=BLUE, width=0.62, label="Independents", zorder=3)
ax.bar(x, actual.chain_closures, bottom=actual.independent_closures + 60, color=ORANGE,
       width=0.62, label="Chains", zorder=3)
f = cl[cl.status == "forecast"].iloc[0]
ax.bar(f.year, f.total_closures, color="none", edgecolor=MUTED, hatch="///", linewidth=1,
       width=0.62, zorder=3, label="2025 forecast (no split)")
for _, r in cl.iterrows():
    ax.text(r.year, r.total_closures + 350, f"{r.total_closures/1000:.1f}k", ha="center",
            fontsize=9.5, color=INK)
ax.set_ylim(0, 20500)
ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5000))
ax.yaxis.set_major_formatter(lambda v, _: f"{v/1000:.0f}k")
ax.set_xticks(list(cl.year))
ax.legend(loc="upper left", ncol=3, fontsize=9.5, bbox_to_anchor=(0, 1.0))
titled(ax, "Independents now account for 5 in 6 store closures",
       "UK store closures per year")
source(fig, "Centre for Retail Research (2018–2024 actual; 2025 forecast)")
save(fig, "02_store_closures.png")

# ---------------------------------------------------------------- 3. Format matters
v = pd.read_csv(DATA / "vacancy_by_location.csv")
fig, ax = plt.subplots(figsize=(9, 5))
series = [("shopping_centres", "Shopping centres", ORANGE),
          ("high_streets", "High streets", BLUE),
          ("retail_parks", "Retail parks", AQUA)]
for col, label, colour in series:
    d = v.dropna(subset=[col])
    ax.plot(d.sort_key, d[col], color=colour, linewidth=2.2, marker="o", markersize=7,
            markeredgecolor=SURFACE, markeredgewidth=1.5, label=label, zorder=3)
    last = d.iloc[-1]
    ax.text(last.sort_key + 0.08, last[col], f"{label}  {last[col]:.1f}%", va="center",
            fontsize=10, color=INK)
pre = v.iloc[0]
ax.axhline(pre.overall_gb, color=MUTED, linewidth=1, linestyle=(0, (4, 3)))
ax.text(2022.0, pre.overall_gb + 0.3, f"GB overall, all locations, before the pandemic (Q4 2019): {pre.overall_gb}%",
        fontsize=9, color=MUTED)
ax.set_xticks(v.sort_key[1:])
ax.set_xticklabels(v.period[1:])
ax.set_xlim(2021.3, 2024.75)
ax.set_ylim(6, 21)
ax.yaxis.set_major_formatter(lambda v_, _: f"{v_:.0f}%")
ax.legend(loc="upper center", ncol=3, fontsize=9.5)
titled(ax, "Retail parks recovered after the pandemic; high streets did not",
       "Share of GB shop units vacant, by location type")
source(fig, "BRC–Local Data Company Vacancy Monitor (latest fully reported quarter: Q4 2023)")
save(fig, "03_vacancy_by_location.png")

# ---------------------------------------------------------------- 4. Where it hurts
r = pd.read_csv(DATA / "vacancy_by_region_q4_2023.csv").iloc[::-1]
fig, ax = plt.subplots(figsize=(9, 3.8))
colours = [MUTED if reg == "GB average" else BLUE for reg in r.region]
ax.barh(r.region, r.vacancy_pct, color=colours, height=0.58, zorder=3)
for i, (reg, val) in enumerate(zip(r.region, r.vacancy_pct)):
    ax.text(val + 0.25, i, f"{val:.1f}%", va="center", fontsize=10.5, color=INK)
ax.set_xlim(0, 21)
ax.grid(axis="y", visible=False)
ax.grid(axis="x", visible=True)
ax.xaxis.set_major_formatter(lambda v_, _: f"{v_:.0f}%")
titled(ax, "Vacancy in the North East is almost 70% higher than in London",
       "Share of shop units vacant, Q4 2023")
source(fig, "Local Data Company")
save(fig, "04_vacancy_by_region.png")

# ---------------------------------------------------------------- 5. Rates: the "cut" is a rise for small shops
RV = 30_000  # illustrative rateable value of a small town-centre shop (above small business rate relief)
bills = pd.DataFrame([
    ("2024/25", 0.499 * (1 - 0.75)),
    ("2025/26", 0.499 * (1 - 0.40)),
    ("2026/27", 0.382),
], columns=["year", "effective_rate"])
bills["bill"] = RV * bills.effective_rate
fig, ax = plt.subplots(figsize=(9, 4.6))
ax.bar(bills.year, bills.bill, color=[MUTED, MUTED, ORANGE], width=0.5, zorder=3)
for i, b in enumerate(bills.bill):
    ax.text(i, b + 250, f"£{b:,.0f}", ha="center", fontsize=12, fontweight="bold", color=INK)
notes = ["49.9p multiplier, 75% RHL relief", "49.9p multiplier, 40% RHL relief", "38.2p RHL multiplier, no relief"]
ax.set_xticks(range(3))
ax.set_xticklabels([f"{y}\n{n}" for y, n in zip(bills.year, notes)], fontsize=9.5)
ax.set_ylim(0, 13500)
ax.yaxis.set_major_formatter(lambda v_, _: f"£{v_/1000:.0f}k")
ax.tick_params(axis="x", pad=4)
titled(ax, "The 'permanent cut' still raises a small shop's bill by 28% on last year",
       f"Annual business rates bill for an illustrative shop with rateable value £{RV:,} (England)")
source(fig, "Armstrong Watson (2024/25–2025/26 reliefs); Spelthorne BC (2026/27 multipliers). Ignores revaluation and transitional relief.")
save(fig, "05_business_rates_example.png")

# ---------------------------------------------------------------- key numbers for the write-up
print("\nKey numbers")
print(f"  Online share: {o[2019]}% (2019) -> {o[2021]}% peak year (2021) -> {o[2025]}% (2025): "
      f"+{o[2025]-o[2019]:.1f} pts on 2019, {(o[2025]-o[2019])/(o[2021]-o[2019]):.0%} of the pandemic jump kept")
c24 = actual[actual.year == 2024].iloc[0]
print(f"  2024 closures: {int(c24.total_closures):,}, independents {int(c24.independent_closures):,} "
      f"({c24.independent_closures/c24.total_closures:.0%})")
print(f"  2018-2024 average closures per year: {actual.total_closures.mean():,.0f}; "
      f"2025 forecast {int(f.total_closures):,} (+{f.total_closures/c24.total_closures-1:.0%} on 2024)")
rp = v.dropna(subset=["retail_parks"])
print(f"  Retail parks: {rp.retail_parks.iloc[0]}% -> {rp.retail_parks.iloc[-1]}%; "
      f"shopping centres: {v.shopping_centres.dropna().iloc[0]}% -> {v.shopping_centres.dropna().iloc[-1]}%; "
      f"high streets {v.high_streets.dropna().iloc[0]}% -> {v.high_streets.dropna().iloc[-1]}%")
ne, ldn = 17.9, 10.6
print(f"  North East vs London vacancy: {ne}% vs {ldn}% ({ne/ldn-1:.0%} higher)")
b = bills.set_index("year").bill
print(f"  Rates bill (RV £{RV:,}): £{b['2024/25']:,.0f} -> £{b['2025/26']:,.0f} -> £{b['2026/27']:,.0f} "
      f"({b['2026/27']/b['2025/26']-1:+.0%} vs 2025/26, {b['2026/27']/b['2024/25']-1:+.0%} vs 2024/25)")
