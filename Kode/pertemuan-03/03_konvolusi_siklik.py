"""Contoh 3.12: konvolusi siklik setelah penambahan nol."""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AKAR = Path(__file__).resolve().parents[2]
GAMBAR = AKAR / "Gambar" / "pertemuan-03"
GAMBAR.mkdir(parents=True, exist_ok=True)
x = np.array([1, 2, 3, 0])
h = np.array([2, 1, 0, 0])
N = len(x)

H = np.array([[h[(r-c) % N] for c in range(N)] for r in range(N)])
y = H @ x
baris_h = np.array([[h[(r-c) % N] for c in range(N)] for r in range(N)])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6), constrained_layout=True)
im = ax1.imshow(baris_h, cmap="Blues", vmin=0, vmax=max(h))
for r in range(N):
    for c in range(N):
        ax1.text(c, r, int(baris_h[r, c]), ha="center", va="center", fontsize=13)
ax1.set(xticks=range(N), yticks=range(N),
        xlabel=r"kolom yang dikalikan dengan $x[k]$", ylabel=r"lag keluaran $n$",
        title=r"Pergeseran siklik $h[(n-k)\,\mathrm{mod}\,4]$")

n = np.arange(N)
ax2.stem(n, y, linefmt="#087F72", markerfmt="o", basefmt="k-")
for i, nilai in enumerate(y):
    ax2.text(i, nilai+.25, str(int(nilai)), ha="center", color="#087F72")
ax2.set(xticks=n, xlabel="$n$", ylabel=r"$y_c[n]$", ylim=(0, 9.5),
        title=r"Hasil $y_c=\{2,5,8,3\}$")
ax2.grid(alpha=.2, axis="y")

for ekstensi in ("svg", "png"):
    fig.savefig(GAMBAR / f"konvolusi-siklik.{ekstensi}", dpi=180,
                bbox_inches="tight", facecolor="white")
plt.close(fig)
print("Matriks sirkulan:\n", H)
print("y_c[n] =", y.tolist())
