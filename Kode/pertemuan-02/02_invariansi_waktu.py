import numpy as np
import matplotlib.pyplot as plt


def x(n):
    return np.maximum(1.0 - np.abs(n) / 3.0, 0.0)


def rata_dua(sinyal, n):
    return 0.5 * (sinyal(n) + sinyal(n - 1))


def penguat_berubah(sinyal, n):
    return n * sinyal(n)


n = np.arange(-5, 11)
n0 = 3


def x_geser(n):
    return x(n - n0)


fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=True)

for ax, sistem, nama in zip(
    axes,
    [rata_dua, penguat_berubah],
    ["Rata-rata dua sampel", "Penguatan y[n] = n x[n]"],
):
    jalur_a = sistem(x_geser, n)
    jalur_b = sistem(x, n - n0)
    galat = np.max(np.abs(jalur_a - jalur_b))
    print(f"{nama}: galat maksimum = {galat:.3e}")

    ax.plot(n, jalur_a, "o-", label="Geser masukan, lalu proses")
    ax.plot(n, jalur_b, "s--", label="Proses, lalu geser keluaran")
    ax.set_ylabel("Keluaran")
    ax.text(0.03, 0.94, nama, transform=ax.transAxes, va="top")
    ax.margins(y=0.3)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right", fontsize=9)

axes[-1].set_xlabel("Indeks n")
fig.tight_layout()
plt.show()
