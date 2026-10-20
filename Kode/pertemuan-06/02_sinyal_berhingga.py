"""Peran posisi indeks nol pada transformasi dua sisi dan satu sisi."""
from ztools import *

x = np.array([1, 2, 5, 7, 0, 1])
n1, n2 = np.arange(6), np.arange(-2, 4)
fig, ax = plt.subplots(2, 1, figsize=(9, 6))
stem(ax[0], n1, x)
stem(ax[1], n2, x)
ax[0].set_title('Sampel pertama berada pada n=0')
ax[1].set_title('Sampel ketiga berada pada n=0')
for p, n in zip(ax, [n1, n2]):
    p.set_xticks(n)
    p.set_ylim(-0.5, 8)
simpan(fig, '02_sinyal_berhingga.png')
for z in [0.7+0.4j, 1.5-0.2j, -1+0.3j]:
    X1 = 1+2/z+5/z**2+7/z**3+1/z**5
    X2 = z*z+2*z+5+7/z+1/z**3
    cocok(zt(x, n1, z), X1)
    cocok(zt(x, n2, z), X2)
    cocok(X2, z*z*X1)
    cocok(zplus(x, n2, z), 5+7/z+1/z**3)
print('Polinomial dua sisi, pergeseran, dan pemotongan satu sisi diperiksa.')
