"""Contoh 3.11: tahapan lipat, geser, kali, dan jumlah."""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AKAR = Path(__file__).resolve().parents[2]
GAMBAR = AKAR / "Gambar" / "pertemuan-03"
GAMBAR.mkdir(parents=True, exist_ok=True)
x = np.array([1, 1])
h = np.array([1, 0, 1, 1])
y = np.convolve(x, h)

k = np.arange(-4, 7)
fig, axes = plt.subplots(len(y), 1, figsize=(9, 10), sharex=True,
                         constrained_layout=True)
for n, ax in enumerate(axes):
    xk = np.where((k >= 0) & (k < len(x)), x[np.clip(k, 0, len(x)-1)], 0)
    indeks_h = n-k
    hgeser = np.where((indeks_h >= 0) & (indeks_h < len(h)),
                      h[np.clip(indeks_h, 0, len(h)-1)], 0)
    produk = xk*hgeser
    ax.stem(k, xk, linefmt="#225D91", markerfmt="o", basefmt="k-", label=r"$x[k]$")
    ax.stem(k, hgeser, linefmt="#B65020", markerfmt="s", basefmt="k-",
            label=fr"$h[{n}-k]$")
    nz = np.flatnonzero(produk)
    if len(nz):
        ax.scatter(k[nz], produk[nz], s=85, facecolors="none", edgecolors="#087F72",
                   linewidths=2.2, label="hasil kali tak nol")
    ax.text(.99, .82, fr"$y[{n}]={int(y[n])}$", transform=ax.transAxes,
            ha="right", color="#087F72", fontsize=12)
    ax.set_ylim(-.15, 1.45); ax.grid(alpha=.18, axis="x")
axes[0].legend(ncol=3, frameon=False, loc="upper left")
axes[-1].set_xlabel("Indeks semu, $k$")

for ekstensi in ("svg", "png"):
    fig.savefig(GAMBAR / f"konvolusi-grafis.{ekstensi}", dpi=180,
                bbox_inches="tight", facecolor="white")
plt.close(fig)
print("y[n] =", y.tolist())
