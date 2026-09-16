import numpy as np
import matplotlib.pyplot as plt

# Nilai pada n < 0 dianggap nol.
# Nol di akhir larik memperlihatkan sisa pengaruh masukan.
x = np.array([3, 6, 0, -3, 0, 0, 0], dtype=float)
n = np.arange(len(x))
y = np.zeros(len(x))

for i in range(len(x)):
    jumlah = 0.0
    for k in range(3):
        if i - k >= 0:
            jumlah = jumlah + x[i - k]
    y[i] = jumlah / 3.0

print(" n      x[n]      y[n]")
for i in range(len(x)):
    print(f"{i:2d}  {x[i]:8.3f}  {y[i]:8.3f}")

fig, axes = plt.subplots(2, 1, figsize=(6, 5), sharex=True)
axes[0].stem(n, x, basefmt="k-")
axes[0].set_ylabel("x[n]")
axes[1].stem(n, y, linefmt="C1-", markerfmt="C1o", basefmt="k-")
axes[1].set_ylabel("y[n]")
axes[1].set_xlabel("Indeks n")
for ax in axes:
    ax.grid(True, alpha=0.3)
    ax.set_xticks(n)
fig.tight_layout()
plt.show()
