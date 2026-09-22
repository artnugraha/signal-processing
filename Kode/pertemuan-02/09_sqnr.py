import numpy as np
import matplotlib.pyplot as plt


n = np.arange(100000)
amplitudo, skala_penuh = 3.8, 4.0
x = amplitudo * np.sin(2 * np.pi * np.sqrt(2) * n / 100)
bits = np.array([3, 4, 6, 8, 10, 12])
sqnr_ukur = []
for bit in bits:
    delta = 2 * skala_penuh / 2**bit
    kode = np.floor((x + skala_penuh) / delta)
    kode = np.clip(kode, 0, 2**bit - 1)
    xq = -skala_penuh + (kode + 0.5) * delta
    px = np.mean(x**2)
    pe = np.mean((xq - x)**2)
    sqnr = 10 * np.log10(px / pe)
    sqnr_ukur.append(sqnr)
    print(f'{bit:2d} bit: SQNR = {sqnr:.3f} dB')
teori = 6.0206 * bits + 1.7609 + 20 * np.log10(amplitudo / skala_penuh)

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(bits, sqnr_ukur, 'o-', label='Pengukuran numerik')
ax.plot(bits, teori, '--', label='Model galat seragam')
ax.set(xlabel='Jumlah bit B', ylabel='SQNR (dB)',
       title='Sinusoid dengan amplitudo 95% skala penuh', xticks=bits)
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
plt.show()
