"""Hubungan radius, sudut, dan orde pole dengan sinyal kausal."""
from ztools import *

n = np.arange(18)
fig, ax = plt.subplots(4, 2, figsize=(10, 12))
for row, p in enumerate([0.5, -0.5, 1.0, 1.15]):
    bidang_z(ax[row, 0], [p], [0], inner=abs(p), limit=1.6,
              title=f'Pole sederhana p={p}')
    stem(ax[row, 1], n, p**n)
    ax[row, 1].set_title(f'Sinyal p^n u[n], p={p}')
simpan(fig, '04a_pole_real.png')
fig, ax = plt.subplots(3, 2, figsize=(10, 9))
theta = np.pi/3
for row, (r, repeated) in enumerate([(0.85, False), (0.85, True), (1.0, True)]):
    poles = [r*np.exp(1j*theta), r*np.exp(-1j*theta)]
    bidang_z(ax[row, 0], poles, inner=r, limit=1.5,
              title=f'Pasangan pole: radius {r}, orde {2 if repeated else 1}')
    values = r**n*np.cos(theta*n)
    if repeated:
        values = n*values
    stem(ax[row, 1], n, values)
    ax[row, 1].set_title(('n ' if repeated else '')+f'({r})^n cos(pi n/3) u[n]')
simpan(fig, '04b_pole_berulang.png')
print('Gambar pole real, kompleks-konjugat, dan berulang dibuat.')
