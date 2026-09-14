import numpy as np
import matplotlib.pyplot as plt

# Sinyal energi: x[n] = 0.8^n u[n]
n = np.arange(0, 101)
x_energy = 0.8**n
partial_energy = np.cumsum(np.abs(x_energy)**2)

E_theory = 1.0 / (1.0 - 0.8**2)
print("Energi numerik =", partial_energy[-1])
print("Energi teori   =", E_theory)

# Sinyal daya: sinusoid dengan amplitudo 3
N0 = 40
n0 = np.arange(N0)
x_power = 3.0 * np.cos(2.0 * np.pi * n0 / N0)
P = np.mean(np.abs(x_power)**2)

print("Daya numerik   =", P)
print("Daya teori     =", 3.0**2 / 2.0)

plt.figure(figsize=(8, 4))
plt.plot(n, partial_energy)
plt.axhline(E_theory, linestyle="--", label="Energi teori")
plt.xlabel("N")
plt.ylabel("Energi parsial")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
