"""Generate a polished 3-step protease-protection assay schematic.

Panels:
  Step 1 – Digitonin: only plasma membrane permeabilized; all proteins intact.
  Step 2 – + Proteinase K: cytosolic proteins degraded; intravesicular protected.
  Step 3 – + Triton X-100 (control): all membranes dissolved; nothing protected.

The figure is intentionally clean and publication-friendly: muted palette,
dashed outlines for permeabilized membranes, a small legend, and a
shared caption above each panel.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyBboxPatch, Ellipse


TITLE_COLOR = "#1a3d66"
CAPTION_COLOR = "#1a3d66"

CELL_FILL = "#d9e7f7"
CELL_EDGE = "#3a6fb0"

VES_A_EDGE = "#c0392b"
VES_A_FILL = "#fde6e3"
VES_B_EDGE = "#1f9a5a"
VES_B_FILL = "#e3f5ea"
VES_C_EDGE = "#6f3a9b"
VES_C_FILL = "#efe4f5"

CYT_PROTEIN = "#6b7a8a"
INT_PROTEIN_A = "#c0392b"
INT_PROTEIN_B = "#1f9a5a"
INT_PROTEIN_C = "#6f3a9b"

PROTK_COLOR = "#e84b2a"

GREEN_OK = "#1f9a5a"
RED_BAD = "#c0392b"
GREY_NEUTRAL = "#808890"


def draw_protein(ax, x, y, color, *, r=0.11, alive=True):
    """Draw a protein as a pair of small circles. If ``alive`` is False the
    protein is drawn dashed + faded to indicate it was degraded."""
    if alive:
        for dx in (-r * 0.9, r * 0.9):
            c = Circle((x + dx, y), r, facecolor=color, edgecolor=color,
                       linewidth=0.8, zorder=5)
            ax.add_patch(c)
    else:
        for dx in (-r * 0.9, r * 0.9):
            c = Circle((x + dx, y), r, facecolor="none",
                       edgecolor=color, linewidth=0.8,
                       linestyle=(0, (1.5, 1.5)), alpha=0.55, zorder=5)
            ax.add_patch(c)


def draw_vesicle(ax, x, y, w, h, edge_color, fill_color, *,
                 intact=True, proteins=None, protein_color=None):
    ls = "-" if intact else (0, (4, 3))
    lw = 1.6 if intact else 1.4
    alpha = 1.0 if intact else 0.85
    e = Ellipse((x, y), w, h, facecolor=fill_color, edgecolor=edge_color,
                linewidth=lw, linestyle=ls, alpha=alpha, zorder=3)
    ax.add_patch(e)
    if proteins:
        for (dx, dy) in proteins:
            draw_protein(ax, x + dx, y + dy, protein_color, alive=True)


def draw_protk(ax, x, y, *, size=0.18):
    """Little red arrow/triangle marker representing Proteinase K."""
    tri = plt.Polygon(
        [[x, y + size],
         [x - size * 0.9, y - size * 0.6],
         [x + size * 0.9, y - size * 0.6]],
        closed=True, facecolor=PROTK_COLOR, edgecolor=PROTK_COLOR,
        linewidth=0.6, zorder=6,
    )
    ax.add_patch(tri)


def draw_cell(ax, cx, cy, *, plasma_intact, membranes_intact,
              show_protk_inside=False, show_protk_outside=False,
              cytosolic_alive=True, intravesicular_alive=True,
              intravesicular_membrane_intact=True):
    rx, ry = 3.1, 2.1
    ls = "-" if plasma_intact else (0, (5, 3))
    cell = Ellipse((cx, cy), rx * 2, ry * 2, facecolor=CELL_FILL,
                   edgecolor=CELL_EDGE, linewidth=1.8, linestyle=ls,
                   zorder=2)
    ax.add_patch(cell)

    cyt_positions = [
        (-2.2, 0.9), (-1.6, -1.2), (0.6, 1.4), (1.9, -0.6),
        (-0.3, -1.6), (2.3, 1.0), (-2.6, -0.2), (0.1, 0.2),
    ]
    for (dx, dy) in cyt_positions:
        draw_protein(ax, cx + dx, cy + dy, CYT_PROTEIN,
                     r=0.09, alive=cytosolic_alive)

    vesicles = [
        {
            "pos": (-1.2, 0.55), "wh": (1.0, 0.75),
            "edge": VES_A_EDGE, "fill": VES_A_FILL,
            "protein_color": INT_PROTEIN_A,
            "proteins": [(-0.1, 0.05), (0.12, 0.05)],
        },
        {
            "pos": (-0.3, -0.75), "wh": (0.95, 0.7),
            "edge": VES_B_EDGE, "fill": VES_B_FILL,
            "protein_color": INT_PROTEIN_B,
            "proteins": [(-0.12, 0.0), (0.12, 0.0)],
        },
        {
            "pos": (1.1, -0.1), "wh": (1.0, 0.75),
            "edge": VES_C_EDGE, "fill": VES_C_FILL,
            "protein_color": INT_PROTEIN_C,
            "proteins": [(-0.12, 0.05), (0.12, -0.05)],
        },
    ]
    for v in vesicles:
        vx, vy = v["pos"]
        w, h = v["wh"]
        draw_vesicle(
            ax, cx + vx, cy + vy, w, h,
            edge_color=v["edge"], fill_color=v["fill"],
            intact=intravesicular_membrane_intact,
            proteins=v["proteins"] if intravesicular_alive else None,
            protein_color=v["protein_color"],
        )
        if not intravesicular_alive:
            for (dx, dy) in v["proteins"]:
                draw_protein(ax, cx + vx + dx, cy + vy + dy,
                             v["protein_color"], alive=False)

    if show_protk_outside:
        for (dx, dy) in [(-3.6, 1.4), (3.5, 1.7), (3.7, -1.4), (-3.5, -1.5),
                         (0.2, 2.3)]:
            draw_protk(ax, cx + dx, cy + dy)

    if show_protk_inside:
        for (dx, dy) in [(-2.0, -0.3), (1.7, 1.1), (0.4, -1.8),
                         (-1.2, 1.6), (2.5, 0.2), (-0.6, 1.2),
                         (1.6, -1.3)]:
            draw_protk(ax, cx + dx, cy + dy)


def draw_panel(ax, *, panel_idx):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.8)
    ax.set_aspect("equal")
    ax.axis("off")

    cx, cy = 5.0, 4.2

    if panel_idx == 0:
        draw_cell(ax, cx, cy,
                  plasma_intact=False,
                  membranes_intact=True,
                  show_protk_inside=False,
                  show_protk_outside=False,
                  cytosolic_alive=True,
                  intravesicular_alive=True,
                  intravesicular_membrane_intact=True)
        caption = "белки на местах"
        caption_color = GREY_NEUTRAL
        header_lines = [
            "Step 1",
            "Дигитонин: проницаема",
            "только плазм. мембрана",
        ]
    elif panel_idx == 1:
        draw_cell(ax, cx, cy,
                  plasma_intact=False,
                  membranes_intact=True,
                  show_protk_inside=True,
                  show_protk_outside=True,
                  cytosolic_alive=False,
                  intravesicular_alive=True,
                  intravesicular_membrane_intact=True)
        caption = "внутри везикул — защищены"
        caption_color = GREEN_OK
        header_lines = [
            "Step 2",
            "+ Proteinase K:",
            "цитозольные белки режутся",
        ]
    else:
        draw_cell(ax, cx, cy,
                  plasma_intact=False,
                  membranes_intact=False,
                  show_protk_inside=True,
                  show_protk_outside=True,
                  cytosolic_alive=False,
                  intravesicular_alive=False,
                  intravesicular_membrane_intact=False)
        caption = "ничего не защищено"
        caption_color = RED_BAD
        header_lines = [
            "Step 3 (контроль)",
            "+ Triton X-100:",
            "все мембраны растворены",
        ]

    y = 7.5
    for i, line in enumerate(header_lines):
        fw = "bold" if i == 0 else "bold"
        fs = 13 if i == 0 else 11.5
        ax.text(5.0, y - i * 0.45, line,
                ha="center", va="center",
                color=CAPTION_COLOR, fontsize=fs, fontweight=fw)

    ax.text(5.0, 0.55, caption,
            ha="center", va="center",
            color=caption_color, fontsize=12, fontweight="bold")


def build_figure(out_path: Path) -> Path:
    fig, axes = plt.subplots(1, 3, figsize=(16.5, 6.2), dpi=160)
    fig.subplots_adjust(left=0.015, right=0.985, top=0.82, bottom=0.14,
                        wspace=0.05)

    fig.suptitle(
        "Протеазная защита: тест на внутривезикулярную локализацию",
        color=TITLE_COLOR, fontsize=18, fontweight="bold", y=0.97,
    )

    for i, ax in enumerate(axes):
        draw_panel(ax, panel_idx=i)

    legend_items = [
        Line2D([0], [0], marker="o", linestyle="",
               markerfacecolor=CYT_PROTEIN, markeredgecolor=CYT_PROTEIN,
               markersize=8, label="цитозольный белок"),
        Line2D([0], [0], marker="o", linestyle="",
               markerfacecolor=INT_PROTEIN_A, markeredgecolor=INT_PROTEIN_A,
               markersize=8, label="внутривезикулярный белок"),
        Line2D([0], [0], marker="^", linestyle="",
               markerfacecolor=PROTK_COLOR, markeredgecolor=PROTK_COLOR,
               markersize=10, label="Proteinase K"),
        Line2D([0], [0], color=CELL_EDGE, linestyle=(0, (5, 3)),
               linewidth=2, label="проницаемая мембрана"),
        Line2D([0], [0], color=CELL_EDGE, linestyle="-",
               linewidth=2, label="интактная мембрана"),
    ]
    fig.legend(handles=legend_items, loc="lower center", ncol=5,
               frameon=False, fontsize=10.5,
               bbox_to_anchor=(0.5, 0.005))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    output = Path(__file__).resolve().parent.parent / "images" / \
        "protease_protection_fixed.png"
    saved = build_figure(output)
    print(f"Saved: {saved}")
