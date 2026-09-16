import numpy as np
import matplotlib.pyplot as plt


def orde_satu(x, a, b, y_awal):
    y = np.zeros(len(x))
    y_lama = y_awal
    for i in range(len(x)):
        y[i] = a * y_lama + b * x[i]
        y_lama = y[i]
    return y


x = np.array([2, 2, 2, 0, 0, 0, 0, 0], dtype=float)
n = np.arange(len(x))
a = 0.5
b = 0.5
q = 1.0

y_total = orde_satu(x, a, b, q)
y_mn = orde_satu(np.zeros(len(x)), a, b, q)
y_kn = orde_satu(x, a, b, 0.0)
galat = np.max(np.abs(y_total - y_mn - y_kn))

print(" n    masukan-nol    keadaan-nol          total")
for i in range(len(x)):
    print(f"{i:2d}  {y_mn[i]:13.6f}  {y_kn[i]:13.6f}  {y_total[i]:13.6f}")
print(f"Galat dekomposisi = {galat:.3e}")
print("Galat respons masukan-nol =",
      np.max(np.abs(y_mn - a**(n + 1) * q)))

plt.figure(figsize=(7, 4.5))
plt.plot(n, y_total, "o-", label="Respons total")
plt.plot(n, y_mn, "s--", label="Respons masukan-nol")
plt.plot(n, y_kn, "^--", label="Respons keadaan-nol")
plt.plot(n, y_mn + y_kn, "kx", markersize=9, label="Jumlah kedua respons")
plt.xlabel("Indeks n")
plt.ylabel("Keluaran")
plt.xticks(n)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
