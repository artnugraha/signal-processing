"""Contoh 3.13–3.15: korelasi silang linear dan siklik."""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AKAR = Path(__file__).resolve().parents[2]
GAMBAR = AKAR / "Gambar" / "pertemuan-03"
GAMBAR.mkdir(parents=True, exist_ok=True)

x1 = np.array([4, 2, -1, 3, -2, -6, -5, 4, 5])
x2 = np.array([-4, 1, 3, 7, 4, -2, -8, -2, 1])
N = len(x1)

lag = np.arange(-(N-1), N)
r_buku = np.array([
    sum(x1[n] * x2[n+j] for n in range(N) if 0 <= n+j < N) / N
    for j in lag
])
pasangan = N - np.abs(lag)
r_tanpa_bias = np.where(pasangan > 0, r_buku*N/pasangan, np.nan)

fig, axes = plt.subplots(2, 1, figsize=(10, 7.2), constrained_layout=True)
n = np.arange(1, N+1)
axes[0].step(n, x1, where="mid", color="#225D91", lw=2, label=r"$x_1[n]$")
axes[0].step(n, x2, where="mid", color="#B65020", lw=2, label=r"$x_2[n]$")
axes[0].scatter(n, x1, color="#225D91"); axes[0].scatter(n, x2, color="#B65020")
axes[0].axhline(0, color="#253442", lw=.8); axes[0].set_xticks(n)
axes[0].set(xlabel="$n$", ylabel="Nilai sampel", title="Data pada Contoh 3.13")
axes[0].grid(alpha=.2); axes[0].legend(frameon=False, ncol=2)

axes[1].stem(lag, r_buku, linefmt="#225D91", markerfmt="o", basefmt="k-",
             label=r"normalisasi tetap $1/N$")
axes[1].plot(lag, r_tanpa_bias, "s--", color="#087F72", label=r"normalisasi $1/(N-|j|)$")
axes[1].axvline(3, color="#B65020", ls=":", lw=2, label="$j=3$")
axes[1].set(xticks=lag, xlabel="Lag, $j$", ylabel="Korelasi silang",
            title="Korelasi sebagai fungsi lag")
axes[1].grid(alpha=.2); axes[1].legend(frameon=False, ncol=3)

for ekstensi in ("svg", "png"):
    fig.savefig(GAMBAR / f"korelasi-lag.{ekstensi}", dpi=180,
                bbox_inches="tight", facecolor="white")
plt.close(fig)

a = np.array([4, 3, 1, 6, 0, 0])
b = np.array([5, 2, 3, 0, 0, 0])
r_siklik = np.array([sum(a[n] * b[(n+j) % 6] for n in range(6)) for j in range(6)])
print("r12(0) =", np.dot(x1, x2)/N)
print("r12(3) dari suku yang tertulis =", r_buku[lag.tolist().index(3)])
print("korelasi siklik a dan b =", r_siklik.tolist())
