"""Integral kontur numerik dan pengambilan koefisien indeks negatif."""
from ztools import *

a, rho = 0.5, 1.2
n = np.arange(-8, 13)
X = lambda z: z/(z-a)
back = invers_kontur(X, n, rho, 1024)
exact = np.where(n >= 0, a**n, 0)
cocok(back, exact)
fig, ax = plt.subplots(1, 2, figsize=(11, 4.8))
bidang_z(ax[0], [a], [0], inner=a, limit=1.7, title='Kontur |z|=1.2 di dalam ROC')
t = np.linspace(0, 2*np.pi, 500)
ax[0].plot(rho*np.cos(t), rho*np.sin(t), color=JINGGA, linewidth=2, label='Kontur invers')
ax[0].annotate('', xy=(rho*np.cos(0.7), rho*np.sin(0.7)),
               xytext=(rho*np.cos(0.4), rho*np.sin(0.4)),
               arrowprops=dict(arrowstyle='->', color=JINGGA, linewidth=2))
ax[0].legend(loc='lower left', fontsize=8)
stem(ax[1], n, exact)
ax[1].plot(n, back.real, 'x', color=JINGGA, label='Integral numerik')
ax[1].set_title('Invers: a^n u[n]')
ax[1].legend()
simpan(fig, '09_integral_invers.png')
print('Galat maksimum integral invers:', np.max(abs(back-exact)))
for rr in [0.7, 1.0, 1.5]:
    cocok(invers_kontur(X, n, rr, 1024), exact)
print('Tiga radius kontur di dalam ROC memberikan hasil yang sama.')
