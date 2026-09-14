import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(-2.0, 2.0, 2001)

def x(t):
    return np.exp(-t) * (t >= 0)

xe = 0.5 * (x(t) + x(-t))
xo = 0.5 * (x(t) - x(-t))

plt.figure(figsize=(9, 7))

plt.subplot(3, 1, 1)
plt.plot(t, x(t))
plt.ylabel("x(t)")
plt.grid(True, alpha=0.3)

plt.subplot(3, 1, 2)
plt.plot(t, xe)
plt.ylabel("x_e(t)")
plt.grid(True, alpha=0.3)

plt.subplot(3, 1, 3)
plt.plot(t, xo)
plt.xlabel("t")
plt.ylabel("x_o(t)")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
