"""Tiga ekspansi dan invers kausalnya, termasuk pole kompleks."""
from ztools import *

points = [2+0.4j, -2+0.7j, 1.8-0.3j]
for z in points:
    F1 = z*z/((z-0.5)*(z-0.75)*(z-1))
    cocok(F1, 2/(z-0.5)-9/(z-0.75)+8/(z-1))
    F2 = 12/((z+1)*(z-1)**2)
    cocok(F2, 3/(z+1)+6/(z-1)**2-3/(z-1))
    F3 = (z+1)/(z*(z-1)*(z*z+2*z+2))
    cocok(F3, -0.5/z+0.4/(z-1)+(0.05+0.15j)/(z+1-1j)
           +(0.05-0.15j)/(z+1+1j))
n = np.arange(17)
x1 = 2*0.5**n-9*0.75**n+8
x2 = 3*(-1.)**n+6*n-3
x3 = -0.5*(n == 0)+0.4+np.sqrt(2)**n*(
    0.1*np.cos(3*np.pi*n/4)-0.3*np.sin(3*np.pi*n/4))
cocok(x1, deret_rasional([1], [1, -2.25, 1.625, -0.375], len(n)))
cocok(x2, deret_rasional([0, 0, 12], [1, -1, -1, 1], len(n)))
cocok(x3, deret_rasional([0, 0, 1, 1], [1, 1, 0, -2], len(n)))
fig, ax = plt.subplots(3, 1, figsize=(10, 8))
for panel, x, title in zip(ax, [x1, x2, x3],
    ['Tiga pole sederhana: komponen menetap', 'Pole ganda pada 1: pertumbuhan ramp',
     'Pole kompleks radius akar(2): osilasi membesar']):
    stem(panel, n, x)
    panel.set_title(title)
simpan(fig, '07_invers_kausal.png')
print('Koefisien sederhana: 2, -9, 8.')
print('Koefisien pole berulang: A=3, B2=6, B1=-3.')
print('Koefisien kompleks: -0.5, 0.4, 0.05+0.15j, 0.05-0.15j.')
cetak('Sampel awal invers kompleks:', x3[:8])
print('Semua invers sesuai dengan koefisien pembagian fungsi rasional.')
