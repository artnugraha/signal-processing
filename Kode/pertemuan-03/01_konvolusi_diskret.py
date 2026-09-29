"""Contoh 3.10: konvolusi dua barisan berhingga."""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AKAR = Path(__file__).resolve().parents[2]
GAMBAR = AKAR / "Gambar" / "pertemuan-03"
GAMBAR.mkdir(parents=True, exist_ok=True)

x = np.array([-2, 0, 1, -1, 3])
h = np.array([1, 2, 0, -1])
y = np.convolve(x, h)
print("y[n] =", y.tolist())

fig, axes = plt.subplots(3, 1, figsize=(9, 6.5), constrained_layout=True)
for ax, data, nama, warna in zip(
        axes, (x, h, y), (r"$x[n]$", r"$h[n]$", r"$y[n]=x[n]*h[n]$"),
        ("#225D91", "#B65020", "#087F72")):
    n = np.arange(len(data))
    markerline, stemlines, baseline = ax.stem(n, data, basefmt="k-")
    plt.setp(markerline, color=warna, markersize=7)
    plt.setp(stemlines, color=warna, linewidth=2)
    ax.axhline(0, color="#253442", linewidth=.8)
    ax.set_ylabel(nama); ax.set_xticks(n); ax.grid(alpha=.2, axis="y")
axes[-1].set_xlabel("Indeks sampel, $n$")

for ekstensi in ("svg", "png"):
    fig.savefig(GAMBAR / f"konvolusi-diskret.{ekstensi}", dpi=180,
                bbox_inches="tight", facecolor="white")
plt.close(fig)
