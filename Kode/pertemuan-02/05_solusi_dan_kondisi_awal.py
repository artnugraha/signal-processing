import numpy as np
import matplotlib.pyplot as plt


def orde_satu(x, a, b, q):
    y = np.zeros(len(x))
    lama = float(q)
    for n in range(len(x)):
        y[n] = a * lama + b * x[n]
        lama = y[n]
    return y


n = np.arange(13)
a, b, q = 0.5, 1.0, 3.0
x = np.ones(len(n))
y_total = orde_satu(x, a, b, q)
y_mn = q * a**(n + 1)
y_kn = b * (1 - a**(n + 1)) / (1 - a)
print('Tiga keluaran pertama:', y_total[:3])
assert np.allclose(y_total, y_mn + y_kn)
assert np.allclose(y_mn, orde_satu(np.zeros(len(n)), a, b, q))
assert np.allclose(y_kn, orde_satu(x, a, b, 0))

fig, ax = plt.subplots(figsize=(8, 4.7))
ax.plot(n, y_total, 'o-', label='Respons total, q = 3')
ax.plot(n, y_mn, 's-', label='Respons masukan-nol')
ax.plot(n, y_kn, '^-', label='Respons keadaan-nol')
ax.axhline(2, color='gray', linestyle='--', label='Solusi partikular = 2')
ax.set(xlabel='Indeks n', ylabel='Keluaran',
       title='Respons keadaan-nol tidak sama dengan solusi partikular')
ax.grid(alpha=0.3)
ax.legend(loc='center right', fontsize=9)
fig.tight_layout()
plt.show()
