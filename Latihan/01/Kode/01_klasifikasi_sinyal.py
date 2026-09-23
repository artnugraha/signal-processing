import numpy as np
import matplotlib.pyplot as plt


# Sinyal waktu-kontinu
t_periodik = np.linspace(-0.5, 0.5, 2001)
t_kausal = np.linspace(-1.0, 3.0, 2001)
x1 = 3 * np.cos(8 * np.pi * t_periodik)
x2 = np.where(t_kausal >= 0, np.exp(-2 * t_kausal), 0.0)

# Sinyal waktu-diskret
n_periodik = np.arange(-20, 21)
n_kausal = np.arange(-5, 21)
x3 = np.cos(np.pi * n_periodik / 4)
x4 = np.sin(np.pi * n_periodik / 5)
x5 = np.where(n_kausal >= 0, 0.7**n_kausal, 0.0)

fig, axes = plt.subplots(5, 1, figsize=(9, 13))

axes[0].plot(t_periodik, x1)
axes[0].set_title(r'$x_1(t)=3\cos(8\pi t)$')
axes[0].set_xlabel(r'$t$ (s)')

axes[1].plot(t_kausal, x2)
axes[1].set_title(r'$x_2(t)=e^{-2t}u(t)$')
axes[1].set_xlabel(r'$t$ (s)')

axes[2].stem(n_periodik, x3)
axes[2].set_title(r'$x_3[n]=\cos(\pi n/4)$')
axes[2].set_xlabel(r'$n$')

axes[3].stem(n_periodik, x4)
axes[3].set_title(r'$x_4[n]=\sin(\pi n/5)$')
axes[3].set_xlabel(r'$n$')

axes[4].stem(n_kausal, x5)
axes[4].set_title(r'$x_5[n]=(0.7)^n u[n]$')
axes[4].set_xlabel(r'$n$')

for ax in axes:
    ax.set_ylabel('Amplitudo')
    ax.axhline(0, color='black', linewidth=0.8)
    ax.grid(alpha=0.3)

fig.tight_layout()
fig.savefig('../Gambar/01-klasifikasi-sinyal.png', dpi=180,
            bbox_inches='tight')
plt.show()
