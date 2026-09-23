import numpy as np
import matplotlib.pyplot as plt


def rectangular(z):
    """Bernilai satu untuk -1 <= z <= 1 dan nol di luar interval."""
    z = np.asarray(z)
    return ((z >= -1) & (z <= 1)).astype(float)


t = np.linspace(-3.5, 4.0, 3001)
sinyal = [
    (rectangular(t), r'$x(t)$'),
    (rectangular(t - 2), r'$x(t-2)$'),
    (rectangular(t + 1), r'$x(t+1)$'),
    (rectangular(-t), r'$x(-t)$'),
    (rectangular(2 * t), r'$x(2t)$'),
    (rectangular(2 * t - 4), r'$y(t)=x(2t-4)$'),
]

fig, axes = plt.subplots(3, 2, figsize=(11, 8), sharex=True, sharey=True)
for ax, (nilai, judul) in zip(axes.flat, sinyal):
    ax.step(t, nilai, where='post', linewidth=2)
    ax.fill_between(t, 0, nilai, step='post', alpha=0.18)
    ax.set_title(judul)
    ax.set_ylim(-0.15, 1.35)
    ax.set_ylabel('Amplitudo')
    ax.set_xlabel(r'$t$')
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.grid(alpha=0.3)

fig.tight_layout()
fig.savefig('../Gambar/08-09-transformasi-waktu.png', dpi=180,
            bbox_inches='tight')
plt.show()
