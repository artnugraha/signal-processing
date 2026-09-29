"""Contoh 3.18: konvolusi dua pulsa persegi dan proses tumpang tindihnya."""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AKAR = Path(__file__).resolve().parents[2]
GAMBAR = AKAR / "Gambar" / "pertemuan-03"
GAMBAR.mkdir(parents=True, exist_ok=True)
a = 1.0
tau = np.linspace(-3*a, 3*a, 2401)
x_tau = (np.abs(tau) <= a).astype(float)
t_kasus = [-2.4*a, -1.2*a, -0.4*a, 0.7*a, 1.5*a, 2.4*a]

fig, axes = plt.subplots(3, 2, figsize=(11, 8), sharex=True, sharey=True,
                         constrained_layout=True)
for ax, t in zip(axes.flat, t_kasus):
    h = (np.abs(t-tau) <= a).astype(float)
    ax.fill_between(tau, 0, np.minimum(x_tau, h), color="#91C9B9", alpha=.75,
                    label="daerah tumpang tindih")
    ax.plot(tau, x_tau, color="#225D91", lw=2, label=r"$x(\tau)$")
    ax.plot(tau, h, color="#B65020", lw=2, ls="--", label=r"$h(t-\tau)$")
    ax.set_title(fr"$t={t/a:.1f}a$")
    ax.grid(alpha=.15); ax.set_ylim(-.08, 1.28)
for ax in axes[-1]: ax.set_xlabel(r"$\tau/a$")
for ax in axes[:, 0]: ax.set_ylabel("Amplitudo")
axes[0, 0].legend(frameon=False, fontsize=9)
for ekstensi in ("svg", "png"):
    fig.savefig(GAMBAR / f"proses-konvolusi-kontinu.{ekstensi}", dpi=180,
                bbox_inches="tight", facecolor="white")
plt.close(fig)

t = np.linspace(-3*a, 3*a, 1201)
y_analitik = np.maximum(0, 2*a-np.abs(t))
dt = tau[1]-tau[0]
y_numerik = np.convolve(x_tau, x_tau, mode="full")*dt
t_numerik = np.linspace(2*tau[0], 2*tau[-1], len(y_numerik))

fig, ax = plt.subplots(figsize=(9, 4.8))
ax.plot(t_numerik, y_numerik, color="#C6CFD6", lw=5, label="integrasi numerik")
ax.plot(t, y_analitik, color="#087F72", lw=2.3, label=r"$2a-|t|$")
ax.scatter([-2*a, 0, 2*a], [0, 2*a, 0], color="#B65020", zorder=3)
ax.set(xlim=(-3*a, 3*a), ylim=(-.05, 2.25*a), xlabel="$t$", ylabel="$y(t)$",
       title=r"$\operatorname{rect}(t/2a)*\operatorname{rect}(t/2a)$")
ax.set_xticks([-2*a, -a, 0, a, 2*a], [r"$-2a$", r"$-a$", "$0$", "$a$", r"$2a$"])
ax.grid(alpha=.2); ax.legend(frameon=False)
for ekstensi in ("svg", "png"):
    fig.savefig(GAMBAR / f"hasil-konvolusi-rect.{ekstensi}", dpi=180,
                bbox_inches="tight", facecolor="white")
plt.close(fig)
print("Galat maksimum numerik:", np.max(np.abs(np.interp(t, t_numerik, y_numerik)-y_analitik)))
