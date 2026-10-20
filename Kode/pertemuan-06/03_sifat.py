"""Linearitas, pergeseran, eksponensial, turunan, dan konvolusi."""
from ztools import *

x = np.array([1, 2, -1, 3])
h = np.array([2, -1, 1])
nx, nh = np.arange(-1, 3), np.arange(3)
alpha = 1.2-0.3j
for z in [0.8+0.3j, 1.3+0.4j, 2-0.2j, -1.2+0.3j]:
    X = zt(x, nx, z)
    cocok(zt(x, nx+2, z), z**(-2)*X)
    cocok(zt(alpha**nx*x, nx, z), zt(x, nx, z/alpha))
    step = 1e-6
    derivative = (zt(x, nx, z+step)-zt(x, nx, z-step))/(2*step)
    cocok(zt(nx*x, nx, z), -z*derivative, 1e-6)
    ny = np.arange(nx[0]+nh[0], nx[-1]+nh[-1]+1)
    cocok(zt(np.convolve(x, h), ny, z), X*zt(h, nh, z))
    cocok(zt(2*x-0.3*x, nx, z), 1.7*X)
a, b = 0.5, 2.0
z = 1.2*np.exp(0.3j)
nr, nl = np.arange(160), -np.arange(1, 161)
cocok(zt(a**nr, nr, z)+zt(-b**nl, nl, z), z/(z-a)+z/(z-b))
fig, ax = plt.subplots(1, 2, figsize=(10, 4.5))
bidang_z(ax[0], [a, b], [0, (a+b)/2], inner=a, outer=b,
          title='Irisan ROC: 0.5 < |z| < 2')
bidang_z(ax[1], [0.75], [0], inner=0.75,
          title='Perkalian 1.5^n: radius 0.5 menjadi 0.75')
for p in ax:
    p.legend(loc='upper left', fontsize=8)
simpan(fig, '03_sifat_roc.png')
print('Seluruh sifat dasar yang diuji sesuai, termasuk ROC cincin.')
