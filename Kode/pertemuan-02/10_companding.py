import numpy as np
import matplotlib.pyplot as plt


def kompres_mu(x, mu=255.0):
    return np.sign(x) * np.log1p(mu * np.abs(x)) / np.log1p(mu)


def ekspansi_mu(v, mu=255.0):
    return np.sign(v) * np.expm1(np.abs(v) * np.log1p(mu)) / mu


def kompres_a(x, a=87.6):
    x = np.asarray(x, dtype=float)
    u = np.abs(x)
    hasil = a * u / (1 + np.log(a))
    besar = u > 1 / a
    hasil[besar] = (1 + np.log(a * u[besar])) / (1 + np.log(a))
    return np.sign(x) * hasil


def kuantisasi_normal(x, bit=8):
    delta = 2.0 / 2**bit
    kode = np.clip(np.floor((x + 1) / delta), 0, 2**bit - 1)
    return -1 + (kode + 0.5) * delta


def sqnr(x, y):
    return 10 * np.log10(np.mean(x**2) / np.mean((y - x)**2))


u = np.linspace(-1, 1, 2001)
assert np.allclose(ekspansi_mu(kompres_mu(u)), u)
n = np.arange(10000)
for amplitudo in [0.01, 0.1, 0.8]:
    x = amplitudo * np.sin(2 * np.pi * np.sqrt(2) * n / 100)
    seragam = kuantisasi_normal(x)
    compand = ekspansi_mu(kuantisasi_normal(kompres_mu(x)))
    print(f'A = {amplitudo}: seragam {sqnr(x, seragam):.2f} dB; '
          f'companding {sqnr(x, compand):.2f} dB')

np_plot = np.arange(120)
x_lemah = 0.01 * np.sin(2 * np.pi * np_plot / 80)
seragam = kuantisasi_normal(x_lemah)
compand = ekspansi_mu(kuantisasi_normal(kompres_mu(x_lemah)))
fig, axes = plt.subplots(2, 1, figsize=(8, 7))
axes[0].plot(u, u, '--', color='gray', label='Tanpa kompresi')
axes[0].plot(u, kompres_mu(u), label='Hukum mu, μ = 255')
axes[0].plot(u, kompres_a(u), ':', linewidth=2, label='Hukum A, A = 87.6')
axes[0].set(xlabel='Amplitudo ternormalisasi u', ylabel='Amplitudo terkompresi')
axes[1].plot(np_plot, x_lemah, color='black', label='Asli, amplitudo 0.01')
axes[1].step(np_plot, seragam, where='mid', label='Seragam 8 bit')
axes[1].plot(np_plot, compand, '--', label='Hukum mu, 8 bit, lalu ekspansi')
axes[1].set(xlabel='Indeks n', ylabel='Amplitudo',
            title='Perbandingan pada sinyal lemah')
for ax in axes:
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
fig.tight_layout()
plt.show()
