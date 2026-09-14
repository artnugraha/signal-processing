import numpy as np
import matplotlib.pyplot as plt

A = 1.0
f = 5.0
fs = 40.0

t = np.linspace(0.0, 1.0, 2000)
x = A * np.cos(2.0 * np.pi * f * t)

n = np.arange(0, int(fs) + 1)
tn = n / fs
xn = A * np.cos(2.0 * np.pi * f * tn)

plt.figure(figsize=(9, 4))
plt.plot(t, x, label="x(t)")
plt.stem(tn, xn, linefmt="C1-", markerfmt="C1o",
         basefmt="k-", label="x[n]")
plt.xlabel("Waktu (s)")
plt.ylabel("Amplitudo")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
