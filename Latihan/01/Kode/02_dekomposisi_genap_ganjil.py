import numpy as np
import matplotlib.pyplot as plt


t = np.linspace(-2, 2, 1001)
x = 2 * np.exp(t) + 3 * np.exp(-t)
x_genap = 5 * np.cosh(t)
x_ganjil = -np.sinh(t)

# Verifikasi numerik x = x_genap + x_ganjil.
galat = np.max(np.abs(x - (x_genap + x_ganjil)))
print(f'Galat maksimum rekonstruksi = {galat:.3e}')

fig, axes = plt.subplots(2, 1, figsize=(8, 7), sharex=True)
axes[0].plot(t, x, label=r'$x(t)$')
axes[0].plot(t, x_genap + x_ganjil, '--',
             label=r'$x_e(t)+x_o(t)$')
axes[0].set_title('Verifikasi rekonstruksi sinyal')

axes[1].plot(t, x_genap, label=r'$x_e(t)=5\cosh t$')
axes[1].plot(t, x_ganjil, label=r'$x_o(t)=-\sinh t$')
axes[1].set_title('Komponen genap dan ganjil')
axes[1].set_xlabel(r'$t$')

for ax in axes:
    ax.set_ylabel('Amplitudo')
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.grid(alpha=0.3)
    ax.legend()

fig.tight_layout()
fig.savefig('../Gambar/04-dekomposisi-genap-ganjil.png', dpi=180,
            bbox_inches='tight')
plt.show()
