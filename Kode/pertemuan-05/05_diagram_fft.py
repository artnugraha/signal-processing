"""Diagram butterfly dan pemisahan genap-ganjil; semua posisi dibuat dengan kode."""
from fourier import *
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

fig, axes = plt.subplots(1, 2, figsize=(12, 4), layout="constrained")
for ax, kind in zip(axes, ["DIT", "DIF"]):
    ax.set_xlim(-0.4, 4.5)
    ax.set_ylim(-0.5, 2.7)
    ax.axis("off")
    ax.set_title(f"Butterfly {kind}", fontweight="bold")
    if kind == "DIT":
        ax.text(0, 2, "a", ha="right", va="center")
        ax.text(0, 0, "b", ha="right", va="center")
        ax.text(0.9, -0.4, "kalikan w", ha="center", fontsize=10)
        ax.add_patch(FancyBboxPatch((0.6, -0.15), 0.6, 0.3,
                                   boxstyle="round,pad=0.05", facecolor="#fff1df"))
        ax.text(0.9, 0, "w", ha="center", va="center")
        segments = [((0.15, 2), (3, 2)), ((0.15, 0), (0.55, 0)),
                    ((1.25, 0), (3, 0)), ((0.4, 2), (3, 0)),
                    ((1.25, 0), (3, 2))]
        out = [r"$a+wb$", r"$a-wb$"]
    else:
        ax.text(0, 2, "a", ha="right", va="center")
        ax.text(0, 0, "b", ha="right", va="center")
        segments = [((0.15, 2), (2.6, 2)), ((0.15, 0), (2.6, 0)),
                    ((0.5, 2), (2.6, 0)), ((0.5, 0), (2.6, 2)),
                    ((2.65, 0), (2.8, 0)), ((3.4, 0), (3.65, 0))]
        ax.add_patch(FancyBboxPatch((2.85, -0.15), 0.5, 0.3,
                                   boxstyle="round,pad=0.05", facecolor="#fff1df"))
        ax.text(3.1, 0, "w", ha="center", va="center", zorder=5)
        ax.text(3.1, -0.4, "kalikan w", ha="center", fontsize=10)
        out = [r"$a+b$", r"$(a-b)w$"]
    for start, end in segments:
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="->",
                                     mutation_scale=12, color=BIRU, linewidth=1.4))
    ax.text(2.35, 2.16, "jumlah (+)", ha="center", fontsize=10)
    ax.text(2.35, -0.4, "selisih (-)", ha="center", fontsize=10)
    ax.text(3.7, 2, out[0], va="center")
    ax.text(3.7, 0, out[1], va="center")
simpan(fig, "05_butterfly.png")

fig, ax = plt.subplots(figsize=(12, 5.8), layout="constrained")
ax.axis("off")
ax.set_xlim(-0.6, 7.6)
ax.set_ylim(-0.6, 4.2)
levels = [
    [(3.5, list(range(8)))],
    [(1.5, [0, 2, 4, 6]), (5.5, [1, 3, 5, 7])],
    [(0.5, [0, 4]), (2.5, [2, 6]), (4.5, [1, 5]), (6.5, [3, 7])],
    [(i, [n]) for i, n in enumerate([0, 4, 2, 6, 1, 5, 3, 7])],
]
for lev, nodes in enumerate(levels):
    y = 3.2-lev
    for xpos, values in nodes:
        text = ", ".join(map(str, values))
        ax.text(xpos, y, text, ha="center", va="center", fontsize=11,
                bbox=dict(boxstyle="round,pad=0.35", facecolor="#e8f2f7", edgecolor=BIRU))
        if lev:
            parent = levels[lev-1][next(i for i, (_, v) in enumerate(levels[lev-1])
                                            if values[0] in v)][0]
            ax.annotate("", xy=(xpos, y+0.2), xytext=(parent, y+0.8),
                        arrowprops=dict(arrowstyle="->", color="#777777"), zorder=0)
ax.set_title("Indeks sampel setelah pembagian genap-ganjil berulang", pad=18)
ax.text(3.5, -0.4, "Urutan akhir: 0, 4, 2, 6, 1, 5, 3, 7 (bit terbalik)", ha="center")
simpan(fig, "06_desimasi.png")
print("Pembalikan bit N=8:", indeks_bit_terbalik(8))
print("Pembalikan bit N=16:", indeks_bit_terbalik(16))
