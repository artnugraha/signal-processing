import numpy as np
import matplotlib.pyplot as plt


def sistem_linear(x):
    x_lama = np.zeros(len(x))
    x_lama[1:] = x[:-1]
    return 2.0 * x - 0.5 * x_lama


def sistem_kuadrat(x):
    return x**2


n = np.arange(8)
x1 = np.array([0, 1, 2, 1, 0, -1, 0, 0], dtype=float)
x2 = np.array([1, 0, -1, 2, 1, 0, 0, 0], dtype=float)
alpha = 1.5
beta = -0.5

fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=True)

for ax, sistem, nama in zip(
    axes,
    [sistem_linear, sistem_kuadrat],
    ["Sistem linear", "Sistem penguadratan"],
):
    langsung = sistem(alpha * x1 + beta * x2)
    terpisah = alpha * sistem(x1) + beta * sistem(x2)
    galat = np.max(np.abs(langsung - terpisah))
    print(f"{nama}: galat maksimum = {galat:.3e}")

    ax.plot(n, langsung, "o-", label="Gabung masukan, lalu proses")
    ax.plot(n, terpisah, "s--", label="Proses terpisah, lalu gabung")
    ax.set_ylabel("Keluaran")
    ax.text(0.03, 0.94, nama, transform=ax.transAxes, va="top")
    ax.margins(y=0.25)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right", fontsize=9)

axes[-1].set_xlabel("Indeks n")
fig.tight_layout()
plt.show()
