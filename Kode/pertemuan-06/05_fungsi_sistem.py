"""Respons impuls dari persamaan selisih dan respons frekuensi."""
from ztools import *

n = np.arange(24)
h = np.empty(len(n))
prev = 0.0
for i in n:
    h[i] = 0.5*prev+2*(i == 0)
    prev = h[i]
cocok(h, 2*0.5**n)
w = np.linspace(-np.pi, np.pi, 1001)
H = 2/(1-0.5*np.exp(-1j*w))
fig, ax = plt.subplots(1, 3, figsize=(12, 4))
bidang_z(ax[0], [0.5], [0], inner=0.5, limit=1.5, title='H(z): pole, zero, dan ROC')
stem(ax[1], n, h)
ax[1].set_title('Respons impuls h[n]')
ax[2].plot(w/np.pi, abs(H), color=BIRU)
ax[2].set(xlabel=r'$\Omega/\pi$', ylabel='Magnitudo H', title='Respons frekuensi')
simpan(fig, '05_fungsi_sistem.png')
cetak('Respons impuls awal:', h[:8])
cocok(2/(1-0.5), 4)
cocok(2/(1+0.5), 4/3)
print('H(1)=4; H(-1)=4/3.')
