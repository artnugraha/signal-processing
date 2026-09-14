import numpy as np
import matplotlib.pyplot as plt

def x(t):
    return np.maximum(1.0 - np.abs(t), 0.0)

t = np.linspace(-4.0, 4.0, 2001)

signals = {
    "x(t)": x(t),
    "x(t - 1)": x(t - 1.0),
    "x(-t)": x(-t),
    "x(2t)": x(2.0 * t),
    "x(t/2)": x(0.5 * t),
}

plt.figure(figsize=(9, 8))

for i, (label, y) in enumerate(signals.items(), start=1):
    plt.subplot(len(signals), 1, i)
    plt.plot(t, y)
    plt.ylabel(label)
    plt.grid(True, alpha=0.3)

plt.xlabel("t")
plt.tight_layout()
plt.show()
