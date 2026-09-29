"""Autokorelasi sinyal acak dan deteksi tunda dengan korelasi silang."""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AKAR = Path(__file__).resolve().parents[2]
GAMBAR = AKAR / "Gambar" / "pertemuan-03"
GAMBAR.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(17)

x_acak = rng.normal(size=600)
r_auto_penuh = np.correlate(x_acak, x_acak, mode="full") / len(x_acak)
lag_penuh = np.arange(-len(x_acak)+1, len(x_acak))
pilih = np.abs(lag_penuh) <= 40

N = 128
x = rng.choice([-1.0, 1.0], size=N)
D, alfa = 23, 0.65
y = np.zeros(N)
y[D:] = alfa*x[:-D]
y += 0.55*rng.normal(size=N)
r_yx = np.correlate(y, x, mode="full")
lag_yx = np.arange(-N+1, N)
D_taksir = int(lag_yx[np.argmax(r_yx)])

fig, axes = plt.subplots(2, 1, figsize=(10, 7.2), constrained_layout=True)
axes[0].plot(lag_penuh[pilih], r_auto_penuh[pilih], color="#225D91", lw=1.8)
axes[0].scatter([0], [r_auto_penuh[len(x_acak)-1]], color="#B65020", zorder=3,
                label="maksimum di lag nol")
axes[0].set(xlabel="Lag, $j$", ylabel=r"$r_{xx}[j]$",
            title="Autokorelasi satu realisasi sinyal acak")
axes[0].grid(alpha=.2); axes[0].legend(frameon=False)

axes[1].plot(lag_yx, r_yx, color="#087F72")
axes[1].axvline(D_taksir, color="#B65020", ls="--",
                label=fr"puncak pada $D={D_taksir}$")
axes[1].set(xlabel="Lag, $j$", ylabel=r"$r_{yx}[j]$",
            title="Deteksi waktu tunda pada model radar/sonar")
axes[1].grid(alpha=.2); axes[1].legend(frameon=False)

for ekstensi in ("svg", "png"):
    fig.savefig(GAMBAR / f"autokorelasi-radar.{ekstensi}", dpi=180,
                bbox_inches="tight", facecolor="white")
plt.close(fig)
print("Tunda sebenarnya:", D, "sampel; taksiran:", D_taksir, "sampel")
