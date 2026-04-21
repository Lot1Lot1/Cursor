"""Generate the experimental design scheme with fixed text-box overflow.

The previous version cut off text in several boxes:
  * the orange "Компартментализация" header,
  * "Triton X-100 контроль" in Биохимия,
  * "Xenopus Wnt8 assay" and "Rescue hITGβ1 mRNA" in Функция,
  * the bottom conclusion "Вывод: …".

Here every box is made wide enough to contain its text, and the whole figure
uses a larger canvas so nothing spills out.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


TITLE_COLOR = "#1a3d66"

Q_COLOR = "#1f4e79"
MORPH_COLOR = "#2f7fbf"
BIOCHEM_COLOR = "#1f9a7a"
COMPART_COLOR = "#c68a1a"
FUNC_COLOR = "#7b2a99"
CONCLUSION_COLOR = "#0f3b4a"


def add_box(ax, x, y, w, h, *, facecolor, title, bullets,
            title_fontsize=12, bullet_fontsize=10,
            title_color="white", bullet_color="white",
            radius=0.08):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={radius}",
        linewidth=1.4,
        facecolor=facecolor, edgecolor=facecolor,
    )
    ax.add_patch(box)

    title_y = y + h - 0.42
    ax.text(x + w / 2, title_y, title,
            ha="center", va="center",
            color=title_color, fontsize=title_fontsize, fontweight="bold")

    if bullets:
        bullet_block_top = title_y - 0.55
        line_step = 0.45
        for i, line in enumerate(bullets):
            ax.text(x + w / 2, bullet_block_top - i * line_step, line,
                    ha="center", va="center",
                    color=bullet_color, fontsize=bullet_fontsize)


def add_arrow(ax, x0, y0, x1, y1, color="#2d4a66", lw=1.6):
    arrow = FancyArrowPatch(
        (x0, y0), (x1, y1),
        arrowstyle="-|>", mutation_scale=16,
        color=color, linewidth=lw,
        shrinkA=2, shrinkB=2,
    )
    ax.add_patch(arrow)


def build_figure(out_path: Path) -> Path:
    fig, ax = plt.subplots(figsize=(16, 9), dpi=160)
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 18)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.suptitle("Схема экспериментального дизайна статьи",
                 color=TITLE_COLOR, fontsize=20, fontweight="bold", y=0.97)

    q_w, q_h = 8.0, 2.4
    q_x = (32 - q_w) / 2
    q_y = 14.2
    q_cx = q_x + q_w / 2
    box = FancyBboxPatch(
        (q_x, q_y), q_w, q_h,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        linewidth=1.4, facecolor=Q_COLOR, edgecolor=Q_COLOR,
    )
    ax.add_patch(box)
    ax.text(q_cx, q_y + q_h / 2,
            "Вопрос: как Wnt влияет\nна FA и ITGβ1?",
            ha="center", va="center",
            color="white", fontsize=14, fontweight="bold")

    col_w = 6.8
    col_h = 4.6
    gap = 0.55
    total_w = 4 * col_w + 3 * gap
    start_x = (32 - total_w) / 2
    col_y = 7.6

    columns = [
        {
            "title": "Морфология",
            "color": MORPH_COLOR,
            "bullets": [
                "• IF микроскопия",
                "• DIC vesicle tracking",
                "• Colocalization",
                "   (GSK3, Zyxin)",
            ],
        },
        {
            "title": "Биохимия",
            "color": BIOCHEM_COLOR,
            "bullets": [
                "• Surface biotinylation",
                "• Western blot",
                "• TfR как контроль",
            ],
        },
        {
            "title": "Компартментализация",
            "color": COMPART_COLOR,
            "bullets": [
                "• Digitonin permeab.",
                "• Proteinase K assay",
                "• Triton X-100 контроль",
            ],
        },
        {
            "title": "Функция",
            "color": FUNC_COLOR,
            "bullets": [
                "• Xenopus Wnt8 assay",
                "• ITGβ1 morpholino",
                "• Rescue hITGβ1 mRNA",
            ],
        },
    ]

    col_centers = []
    for i, col in enumerate(columns):
        x = start_x + i * (col_w + gap)
        add_box(ax, x, col_y, col_w, col_h,
                facecolor=col["color"],
                title=col["title"],
                bullets=col["bullets"],
                title_fontsize=13, bullet_fontsize=10.5)
        col_centers.append((x + col_w / 2, col_y + col_h))

    for cx, top_y in col_centers:
        add_arrow(ax, q_cx, q_y, cx, top_y, color="#2d4a66", lw=1.8)

    concl_w = 20.0
    concl_h = 3.6
    concl_x = (32 - concl_w) / 2
    concl_y = 1.1
    concl_cx = concl_x + concl_w / 2
    box = FancyBboxPatch(
        (concl_x, concl_y), concl_w, concl_h,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        linewidth=1.4, facecolor=CONCLUSION_COLOR, edgecolor=CONCLUSION_COLOR,
    )
    ax.add_patch(box)
    ax.text(concl_cx, concl_y + concl_h / 2,
            "Вывод: Wnt за минуты запускает эндоцитоз FA/ITGβ1\n"
            "через ESCRT/MVB, что важно для Wnt-ответа in vivo",
            ha="center", va="center",
            color="white", fontsize=13, fontweight="bold")

    for cx, _ in col_centers:
        add_arrow(ax, cx, col_y, concl_cx, concl_y + concl_h,
                  color="#2d4a66", lw=1.6)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    output = Path(__file__).resolve().parent.parent / "images" / \
        "experimental_design_fixed.png"
    saved = build_figure(output)
    print(f"Saved: {saved}")
