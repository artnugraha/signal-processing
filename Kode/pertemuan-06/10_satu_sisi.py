"""Pemotongan waktu negatif dan suku batas pada pergeseran satu sisi."""
from ztools import *

x = np.array([1, 2, 5, 7, 0, 1])
n = np.arange(-2, 4)
fig, ax = plt.subplots(3, 1, figsize=(10, 9))
stem(ax[0], n, x)
ax[0].axvline(-0.5, linestyle='--', color=JINGGA)
ax[0].set_title('Sinyal berhingga: sampel pada n<0 tidak masuk X+(z)')
a = 0.8
nn = np.arange(10)
stem(ax[1], nn, a**(nn-2))
ax[1].set_title('x[n]=a^n untuk semua n: x[n-2] memiliki riwayat negatif')
shift_causal = np.where(nn >= 2, a**(nn-2), 0)
stem(ax[2], nn, shift_causal)
ax[2].set_title('x[n]=a^n u[n]: penundaan dua sampel memiliki dua nol awal')
simpan(fig, '10_satu_sisi.png')
nn = np.arange(180)
for z in [1.3+0.2j, 1.6-0.3j, -1.4+0.2j]:
    Xp = 1/(1-a/z)
    delay = z**(-2)*Xp+a**(-1)/z+a**(-2)
    advance = z*z*Xp-z*z-a*z
    cocok(delay, a**(-2)*Xp)
    cocok(advance, a*a*Xp)
    cocok(zt(a**(nn-2), nn, z), delay)
    cocok(zt(a**(nn+2), nn, z), advance)
    cocok(zplus(x, n, z), 5+7/z+1/z**3)
    cocok(zplus(x, n+2, z), z**(-2)*zplus(x, n, z)+2/z+1)
print('Suku batas kedua arah dan transformasi satu sisi sinyal berhingga sesuai.')
