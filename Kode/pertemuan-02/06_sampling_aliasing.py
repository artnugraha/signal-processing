import numpy as np
import matplotlib.pyplot as plt


f0 = 70.0
t = np.linspace(0, 0.1, 2001)
analog = np.cos(2 * np.pi * f0 * t)
fig, axes = plt.subplots(2, 1, figsize=(9, 6.5), sharex=True)

for ax, fs in zip(axes, [200.0, 100.0]):
    n = np.arange(int(round(0.1 * fs)) + 1)
    ts = n / fs
    x = np.cos(2 * np.pi * f0 * ts)
    ax.plot(t, analog, color='C0', label='Analog 70 Hz')
    if fs == 100:
        alias = np.cos(2 * np.pi * 30 * t)
        ax.plot(t, alias, '--', color='C1', label='Analog 30 Hz')
        galat = np.max(np.abs(x - np.cos(2 * np.pi * 30 * ts)))
        print('Selisih sampel 70 Hz dan 30 Hz:', galat)
        assert galat < 1e-12
    ax.plot(ts, x, 'ko', markersize=5, label='Sampel')
    ax.set_ylabel('Amplitudo')
    ax.set_title(f'fs = {fs:g} Hz; frekuensi Nyquist = {fs / 2:g} Hz')
    ax.grid(alpha=0.3)
    ax.legend(loc='upper right', fontsize=8)
axes[-1].set_xlabel('Waktu t (s)')
fig.tight_layout()
plt.show()
