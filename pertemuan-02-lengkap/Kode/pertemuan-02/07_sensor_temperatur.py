import numpy as np
import matplotlib.pyplot as plt

n = np.arange(180)
rng = np.random.default_rng(7)
s = 25.0 + 0.4 * np.sin(2.0 * np.pi * n / 100.0)
s = s + 2.0 * (n >= 80)
derau = 0.35 * rng.standard_normal(len(n))
x = s + derau

# Empat sampel sebelum rekaman diasumsikan bernilai 25.
L = 5
y_rata = np.zeros(len(x))
for i in range(len(x)):
    jumlah = 0.0
    for k in range(L):
        if i - k >= 0:
            jumlah = jumlah + x[i - k]
        else:
            jumlah = jumlah + 25.0
    y_rata[i] = jumlah / L

# Keluaran awal rekursif juga diisi 25.
a = 0.8
y_rek = np.zeros(len(x))
y_lama = 25.0
for i in range(len(x)):
    y_rek[i] = a * y_lama + (1.0 - a) * x[i]
    y_lama = y_rek[i]

fig, axes = plt.subplots(2, 1, figsize=(9, 7))
for ax in axes:
    ax.plot(n, x, color="0.7", linewidth=1, label="Data pengukuran")
    ax.plot(n, s, "k--", linewidth=1.6, label="Temperatur acuan")
    ax.plot(n, y_rata, linewidth=1.7, label="Rata-rata 5 sampel")
    ax.plot(n, y_rek, linewidth=1.7, label="Rekursif, a = 0.8")
    ax.axvline(80, color="0.4", linestyle=":")
    ax.set_ylabel("Temperatur (derajat Celsius)")
    ax.set_xlabel("Indeks n")
    ax.grid(True, alpha=0.3)

axes[0].legend(loc="upper left", ncol=2, fontsize=9)
axes[1].set_xlim(65, 105)
fig.tight_layout()
plt.show()
