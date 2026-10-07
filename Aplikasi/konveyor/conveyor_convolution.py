"""Rectangular sensor pulse, ADC, and causal moving-average convolution.
Run with Python 3, NumPy, and Matplotlib. The ideal pulse is a teaching model;
real analogue conditioning rounds the pulse edges before sampling.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fs = 10.0
Ts = 1/fs
n = np.arange(8)
# Ideal pulse: 3 V for 0.2 <= t < 0.6 s. Explicit indices avoid float-boundary issues.
v_samples = np.where((n >= 2) & (n < 6), 3.0, 0.0)
# Endpoint-inclusive teaching ADC model: 256 levels from 0 to 5 V.
# An actual ADC's transition thresholds and coding depend on its specification.
q = np.rint(255*np.clip(v_samples, 0, 5)/5).astype(int)
x = 5*q/255
h = np.ones(3)/3
y = np.convolve(x, h, mode='full')
ny = np.arange(len(y))
assert np.array_equal(q, [0, 0, 153, 153, 153, 153, 0, 0])
assert np.allclose(y, [0, 0, 1, 2, 3, 3, 2, 1, 0, 0])
flag = y >= 2
rising = flag & ~np.r_[False, flag[:-1]]
assert np.flatnonzero(rising).tolist() == [3]

plt.rcParams.update({'font.size': 11, 'axes.grid': True, 'grid.alpha': .25})
fig, ax = plt.subplots(3, 1, figsize=(9, 8), sharex=True)
ax[0].plot([0,.2,.2,.6,.6,.9], [0,0,3,3,0,0], color='tab:blue', lw=2)
ax[0].set(title='1. Ideal analogue sensor pulse', ylabel='Voltage (V)', ylim=(-.25,3.5))
ax[1].stem(n*Ts, x, linefmt='C1-', markerfmt='C1o', basefmt='k-')
for ti, vi, code in zip(n*Ts,x,q):
    ax[1].annotate(str(code), (ti,vi), xytext=(0,8), textcoords='offset points', ha='center', fontsize=9)
ax[1].set(title='2. ADC samples (labels show 8-bit codes)', ylabel='Decoded voltage (V)', ylim=(-.25,3.7))
ax[2].stem(ny*Ts, y, linefmt='C2-', markerfmt='C2o', basefmt='k-')
ax[2].axhline(2, color='tab:red', ls='--', label='Detection threshold: 2 V')
ax[2].set(title='3. Convolution with h = [1/3, 1/3, 1/3]', ylabel='Filtered value (V)', xlabel='Time (s)', ylim=(-.25,3.7))
ax[2].legend(loc='upper right')
fig.tight_layout()
fig.savefig(Path(__file__).with_name('conveyor_convolution.png'), dpi=170)
print('ADC codes:',q)
print('Decoded samples:',x)
print('Convolution:',y)
print('Object counted at sample:',np.flatnonzero(rising))
