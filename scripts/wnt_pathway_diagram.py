"""Generate the Wnt pathway diagram with fixed β-catenin → деградация box.

The previous version cut the text "β-catenin → деградация" on the right side of
the Wnt OFF panel. Here we widen that box (and keep it fully inside the panel)
and re-export the PNG.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


# -- Color palette (matches the original figure) --------------------------------
OFF_BG = "#fbe5e5"
OFF_EDGE = "#c0392b"
OFF_MEMBRANE = "#c0392b"
OFF_FZ = "#6e1a1a"
OFF_LRP = "#8e2a2a"
OFF_DESTRUCTION = "#b03a3a"
OFF_BETA = "#5e1a1a"

ON_BG = "#e8f1fb"
ON_EDGE = "#2e6fb5"
ON_MEMBRANE = "#2e6fb5"
ON_WNT = "#1f7a6b"
ON_FZ = "#2b4a7a"
ON_LRP = "#3a6aa5"
ON_SIGNAL = "#6fa8dc"
ON_MVB = "#7e3a9b"
ON_BETA = "#2aa07a"
ON_TEXT = "#1f7a5a"

TITLE_COLOR = "#1a1f57"


def add_box(ax, x, y, w, h, *, facecolor, edgecolor, text, text_color="white",
            fontsize=11, fontweight="bold", radius=0.05):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.015,rounding_size={radius}",
        linewidth=1.4,
        facecolor=facecolor,
        edgecolor=edgecolor,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text,
            ha="center", va="center",
            color=text_color, fontsize=fontsize, fontweight=fontweight)


def add_arrow(ax, x0, y0, x1, y1, color="black", lw=1.6):
    arrow = FancyArrowPatch(
        (x0, y0), (x1, y1),
        arrowstyle="-|>", mutation_scale=14,
        color=color, linewidth=lw,
    )
    ax.add_patch(arrow)


def draw_off_panel(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")

    panel = FancyBboxPatch(
        (0.15, 0.15), 9.7, 9.2,
        boxstyle="round,pad=0.02,rounding_size=0.18",
        linewidth=1.6, facecolor=OFF_BG, edgecolor=OFF_EDGE,
    )
    ax.add_patch(panel)

    ax.text(5, 9.9, "Wnt OFF", ha="center", va="center",
            color=TITLE_COLOR, fontsize=16, fontweight="bold")
    ax.text(5, 9.35, "β-катенин деградирует", ha="center", va="center",
            color=TITLE_COLOR, fontsize=13, fontweight="bold")

    ax.add_patch(Rectangle((0.15, 7.35), 9.7, 0.9,
                           facecolor="#f2cccc", edgecolor=OFF_MEMBRANE,
                           linewidth=1.4))
    ax.text(5, 7.8, "мембрана", ha="center", va="center",
            color=OFF_EDGE, fontsize=10, fontweight="bold")

    add_box(ax, 0.7, 6.25, 1.4, 0.85, facecolor=OFF_FZ,
            edgecolor=OFF_FZ, text="Fz", fontsize=12)
    add_box(ax, 2.4, 6.25, 1.7, 0.85, facecolor=OFF_LRP,
            edgecolor=OFF_LRP, text="LRP6", fontsize=12)
    ax.text(6.1, 6.65, "нет Wnt", ha="center", va="center",
            color=OFF_EDGE, fontsize=11, fontweight="bold")

    add_box(ax, 1.4, 3.8, 7.2, 1.6,
            facecolor=OFF_DESTRUCTION, edgecolor=OFF_DESTRUCTION,
            text="Destruction complex:\nAxin + APC + CK1 + GSK3",
            fontsize=12)

    add_arrow(ax, 5.0, 3.78, 5.0, 2.85, color=OFF_EDGE, lw=1.8)

    add_box(ax, 1.4, 1.95, 7.2, 0.9,
            facecolor=OFF_BETA, edgecolor=OFF_BETA,
            text="β-catenin → деградация", fontsize=12)

    ax.text(5, 1.15, "нет транскрипции Wnt-генов", ha="center", va="center",
            color=OFF_EDGE, fontsize=10, fontweight="bold", style="italic")


def draw_on_panel(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")

    panel = FancyBboxPatch(
        (0.15, 0.15), 9.7, 9.2,
        boxstyle="round,pad=0.02,rounding_size=0.18",
        linewidth=1.6, facecolor=ON_BG, edgecolor=ON_EDGE,
    )
    ax.add_patch(panel)

    ax.text(5, 9.9, "Wnt ON", ha="center", va="center",
            color=TITLE_COLOR, fontsize=16, fontweight="bold")
    ax.text(5, 9.35, "β-катенин стабилизируется", ha="center", va="center",
            color=TITLE_COLOR, fontsize=13, fontweight="bold")

    add_box(ax, 0.7, 8.35, 1.5, 0.75, facecolor=ON_WNT,
            edgecolor=ON_WNT, text="Wnt", fontsize=12)

    add_arrow(ax, 1.8, 8.3, 2.3, 7.55, color=ON_EDGE, lw=1.8)

    ax.add_patch(Rectangle((0.15, 7.0), 9.7, 0.08,
                           facecolor=ON_MEMBRANE, edgecolor=ON_MEMBRANE))

    add_box(ax, 1.8, 6.1, 1.4, 0.85, facecolor=ON_FZ,
            edgecolor=ON_FZ, text="Fz", fontsize=12)
    add_box(ax, 3.4, 6.1, 1.7, 0.85, facecolor=ON_LRP,
            edgecolor=ON_LRP, text="LRP6", fontsize=12)
    add_box(ax, 5.3, 6.1, 3.9, 0.85, facecolor=ON_SIGNAL,
            edgecolor=ON_SIGNAL, text="сигналосома + DVL", fontsize=11)

    add_arrow(ax, 5.0, 6.05, 5.0, 5.0, color=ON_EDGE, lw=1.8)

    add_box(ax, 1.8, 3.55, 6.4, 1.5,
            facecolor=ON_MVB, edgecolor=ON_MVB,
            text="MVB: GSK3 + Axin\nсеквестрированы (ESCRT)",
            fontsize=12)

    add_arrow(ax, 5.0, 3.52, 5.0, 2.75, color=ON_EDGE, lw=1.8)

    add_box(ax, 2.2, 1.85, 5.6, 0.9,
            facecolor=ON_BETA, edgecolor=ON_BETA,
            text="β-catenin стабилен", fontsize=12)

    ax.text(5, 1.0, "ядро → TCF/LEF → транскрипция",
            ha="center", va="center",
            color=ON_TEXT, fontsize=11, fontweight="bold")


def build_figure(out_path: Path) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(14, 7.2), dpi=160)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.02,
                        wspace=0.06)

    fig.suptitle("Канонический Wnt-путь: базовые состояния",
                 color=TITLE_COLOR, fontsize=18, fontweight="bold", y=0.97)

    draw_off_panel(axes[0])
    draw_on_panel(axes[1])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    output = Path(__file__).resolve().parent.parent / "images" / \
        "wnt_pathway_fixed.png"
    saved = build_figure(output)
    print(f"Saved: {saved}")
