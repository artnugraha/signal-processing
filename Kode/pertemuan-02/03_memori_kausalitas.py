import numpy as np
import matplotlib.pyplot as plt


def kausal(x):
    z = np.pad(x, (2, 0))
    return (z[2:] + z[1:-1] + z[:-2]) / 3


def terpusat(x):
    z = np.pad(x, (1, 1))
    return (z[:-2] + z[1:-1] + z[2:]) / 3


n = np.arange(16)
n0 = 7
x1 = np.sin(0.4 * n)
x2 = x1.copy()
x2[n > n0] += 2.0

fig, axes = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
axes[0].plot(n, x1, 'o-', label='Masukan 1')
axes[0].plot(n, x2, 's--', label='Masukan 2')
axes[0].set_title('Kedua masukan identik sampai n = 7')

for ax, fungsi, nama in zip(axes[1:], [kausal, terpusat],
                          ['Rata-rata kausal', 'Rata-rata terpusat']):
    y1, y2 = fungsi(x1), fungsi(x2)
    beda = np.flatnonzero(~np.isclose(y1, y2))
    print(nama, ': keluaran pertama berbeda pada n =', beda[0])
    ax.plot(n, y1, 'o-', label='Keluaran 1')
    ax.plot(n, y2, 's--', label='Keluaran 2')
    ax.set_title(nama)

for ax in axes:
    ax.axvline(n0, color='gray', linestyle=':', label='Batas n = 7')
    ax.set_ylabel('Amplitudo')
    ax.grid(alpha=0.3)
    ax.legend(loc='upper left', fontsize=8)
axes[-1].set_xlabel('Indeks n')
fig.tight_layout()
plt.show()
