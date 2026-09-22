import numpy as np
import matplotlib.pyplot as plt


def kuantisasi(x, bit, vmin, vmax):
    if not isinstance(bit, (int, np.integer)) or bit < 1 or vmax <= vmin:
        raise ValueError('Bit harus positif dan vmax harus melebihi vmin')
    x = np.asarray(x, dtype=float)
    tingkat = 2**bit
    delta = (vmax - vmin) / tingkat
    indeks = np.floor((x - vmin) / delta)
    kode = np.clip(indeks, 0, tingkat - 1).astype(int)
    xq = vmin + (kode + 0.5) * delta
    return kode, xq


bit, vmin, vmax = 3, -4.0, 4.0
delta = (vmax - vmin) / 2**bit
x = np.array([1.3, 3.6, 2.3, 0.7, -0.7, -2.4, -3.4])
kode, xq = kuantisasi(x, bit, vmin, vmax)
galat = xq - x
print('Masukan  Kuantisasi  Galat  Kode')
for xi, qi, ei, ki in zip(x, xq, galat, kode):
    print(f'{xi:7.1f} {qi:10.1f} {ei:6.1f}  {ki:0{bit}b}')
assert np.max(np.abs(galat)) <= delta / 2

fig, axes = plt.subplots(3, 1, figsize=(8, 8.5))
uji = np.linspace(-5, 5, 2001)
_, tangga = kuantisasi(uji, bit, vmin, vmax)
axes[0].plot(uji, tangga, label='Kuantisator mid-rise')
axes[0].plot(uji, uji, '--', color='gray', label='Identitas')
axes[0].axvspan(-5, vmin, color='C1', alpha=0.15)
axes[0].axvspan(vmax, 5, color='C1', alpha=0.15)
axes[0].set(xlabel='Masukan (V)', ylabel='Keluaran (V)',
            title='Rentang nominal -4 sampai 4 V; saturasi di luar rentang')
n = np.arange(len(x))
axes[1].plot(n, x, 'o-', label='Sampel asli')
axes[1].plot(n, xq, 's--', label='Hasil kuantisasi')
axes[1].set(xlabel='Indeks n', ylabel='Tegangan (V)')
axes[2].stem(n, galat)
axes[2].axhline(delta / 2, color='C1', linestyle='--', label='Batas ±Δ/2')
axes[2].axhline(-delta / 2, color='C1', linestyle='--')
axes[2].set(xlabel='Indeks n', ylabel='Galat (V)', ylim=(-0.65, 0.65))
for ax in axes:
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
fig.tight_layout()
plt.show()
