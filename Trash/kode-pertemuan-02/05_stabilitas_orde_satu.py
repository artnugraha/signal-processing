import numpy as np
import matplotlib.pyplot as plt

n = np.arange(40)
x = np.ones(len(n))
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

for a in [0.5, 0.9, 1.0, 1.05]:
    y = np.zeros(len(x))
    y_lama = 0.0
    for i in range(len(x)):
        y[i] = a * y_lama + x[i]
        y_lama = y[i]

    if a < 1.0:
        ax = axes[0]
        ax.axhline(1.0 / (1.0 - a), color="gray", linestyle=":")
    else:
        ax = axes[1]
    ax.plot(n, y, "o-", markersize=3, label=f"a = {a:g}")
    print(f"a = {a:4.2f}, y[39] = {y[-1]:.6f}")

for ax in axes:
    ax.set_xlabel("Indeks n")
    ax.set_ylabel("y[n]")
    ax.grid(True, alpha=0.3)
    ax.legend()

axes[0].text(0.97, 0.08, "Garis titik: nilai akhir",
             ha="right", transform=axes[0].transAxes)
fig.tight_layout()
plt.show()
