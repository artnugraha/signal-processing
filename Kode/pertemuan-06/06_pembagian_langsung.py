"""Koefisien ekspansi dalam pangkat negatif dan positif z."""
from ztools import *

right = deret_rasional([1], [1, -1.5, 0.5], 16)
left = deret_rasional([0, 0, 1], [0.5, -1.5, 1], 10)
cocok(right[:5], [1, 1.5, 1.75, 1.875, 1.9375])
cocok(left[:7], [0, 0, 2, 6, 14, 30, 62])
fig, ax = plt.subplots(2, 1, figsize=(9, 6))
stem(ax[0], np.arange(len(right)), right.real)
ax[0].set_title('ROC |z| > 1: koefisien z^(-m) adalah x[m]')
stem(ax[1], -np.arange(len(left)), left.real)
ax[1].set_title('ROC |z| < 0.5: koefisien z^m adalah x[-m]')
simpan(fig, '06_pembagian_langsung.png')
cetak('Koefisien sisi kanan:', right[:8])
cetak('Koefisien pangkat positif z:', left[:8])
