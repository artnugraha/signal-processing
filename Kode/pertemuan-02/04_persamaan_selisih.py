import numpy as np
import matplotlib.pyplot as plt


def persamaan_selisih(x, a, b, y_awal=None, x_awal=None):
    x = np.asarray(x, dtype=float)
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.ndim != 1 or b.ndim != 1 or len(a) == 0 or len(b) == 0:
        raise ValueError('a dan b harus berupa vektor yang tidak kosong')
    if a[0] == 0 or x.ndim != 1:
        raise ValueError('a[0] harus tidak nol dan x harus berupa vektor')
    ny, nx = len(a) - 1, len(b) - 1
    yh = np.zeros(ny) if y_awal is None else np.array(y_awal, dtype=float)
    xh = np.zeros(nx) if x_awal is None else np.array(x_awal, dtype=float)
    if yh.shape != (ny,) or xh.shape != (nx,):
        raise ValueError('Panjang riwayat tidak sesuai dengan koefisien')
    y = np.zeros(len(x))
    for n in range(len(x)):
        maju = b[0] * x[n] + np.dot(b[1:], xh)
        balik = np.dot(a[1:], yh)
        y[n] = (maju - balik) / a[0]
        if ny:
            yh[1:] = yh[:-1].copy()
            yh[0] = y[n]
        if nx:
            xh[1:] = xh[:-1].copy()
            xh[0] = x[n]
    return y


n = np.arange(21)
x = 0.5**n
y = persamaan_selisih(x, [1, -0.75, 0.125], [1], y_awal=[1, 0])
y_rumus = (1 + 2 * n) * 0.5**n + 0.75 * 0.25**n
print('Tiga keluaran pertama:', y[:3])
print('Galat maksimum:', np.max(np.abs(y - y_rumus)))
assert np.allclose(y, y_rumus)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(n, y, 'o', label='Iterasi persamaan selisih')
ax.plot(n, y_rumus, '--', label='Solusi analitis')
ax.set(xlabel='Indeks n', ylabel='Keluaran y[n]',
       title='Orde dua dengan kondisi awal y[-1] = 1, y[-2] = 0')
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
plt.show()
