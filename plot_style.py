import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

COLORS = {
    "Sand": "#E9C46A",   # warm sand/ochre
    "Silt": "#2A9D8F",   # teal
    "Clay": "#E07A5F",   # terracotta
}
LINE_COLOR = "#264653"

plt.rcParams.update({
    "axes.edgecolor": "#CBD5E1",
    "axes.labelcolor": "#334155",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#E2E8F0",
    "grid.linewidth": 0.8,
    "xtick.color": "#64748B",
    "ytick.color": "#64748B",
    "font.size": 10,
})


def add_header(ax, text):
    """Draw a gray strip above a plot and write a line of text in it."""
    ax.add_patch(Rectangle((0, 1.03), 1, 0.14, transform=ax.transAxes,
                           facecolor="#F1F5F9", edgecolor="#E2E8F0", clip_on=False))
    ax.text(0.03, 1.10, text, transform=ax.transAxes,
            va="center", fontsize=9, color="#334155")