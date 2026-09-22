import numpy as np
import matplotlib.pyplot as plt


fs, f0 = 40.0, 5.0
ts = np.arange(13) / fs
x = np.sin(2 * np.pi * f0 * ts)
t = np.linspace(0, ts[-1], 3001)
analog = np.sin(2 * np.pi * f0 * t)
print('Empat sampel pertama:', x[:4])
print('Nilai yang ditahan pada t = 0.037 s:', x[int(0.037 * fs)])

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(t, analog, label='Sinyal analog')
ax.step(ts, x, where='post', linewidth=2, label='Penahanan orde nol')
ax.plot(ts, x, 'ko', markersize=5, label='Nilai sampel')
ax.set(xlabel='Waktu t (s)', ylabel='Amplitudo',
       title='Sample-and-hold: f0 = 5 Hz, fs = 40 Hz')
ax.grid(alpha=0.3)
ax.legend(loc='lower left', fontsize=9)
fig.tight_layout()
plt.show()
