"""Eksponensial kanan dan kiri dengan ekspresi rasional sama."""
from ztools import *

a = 0.5
fig, ax = plt.subplots(2, 2, figsize=(10, 7.5))
bidang_z(ax[0, 0], [a], [0], inner=a, limit=1.4,
          title='Sisi kanan: ROC |z| > 0.5')
bidang_z(ax[0, 1], [a], [0], outer=a, limit=1.4,
          title='Sisi kiri: ROC |z| < 0.5')
for p in ax[0]:
    p.legend(loc='upper left', fontsize=8)
n = np.arange(-8, 9)
right = np.where(n >= 0, a**n, 0)
left = np.where(n <= -1, -a**n, 0)
stem(ax[1, 0], n, right)
stem(ax[1, 1], n, left)
ax[1, 0].set_title(r'$a^n u[n]$, a=0.5')
ax[1, 1].set_title(r'$-a^n u[-n-1]$, a=0.5')
simpan(fig, '01_roc_eksponensial.png')
n = np.arange(160)
z = 1.2*np.exp(0.4j)
cocok(zt(a**n, n, z), z/(z-a))
n = -np.arange(1, 161)
z = 0.2*np.exp(0.4j)
cocok(zt(-a**n, n, z), z/(z-a))
print('Transformasi kanan dan kiri sesuai pada titik di dalam ROC masing-masing.')
