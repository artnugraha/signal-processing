"""Satu ekspresi rasional dengan tiga ROC dan tiga sinyal berbeda."""
from ztools import *

n = np.arange(-8, 9)
right = np.where(n >= 0, 2-0.5**n, 0)
left = np.where(n <= -1, -2+0.5**n, 0)
both = np.where(n <= -1, -2, -0.5**n)
fig, ax = plt.subplots(3, 2, figsize=(10, 11))
specs = [(1, np.inf, '|z| > 1'), (0, 0.5, '|z| < 0.5'), (0.5, 1, '0.5 < |z| < 1')]
for row, (values, (inner, outer, title)) in enumerate(zip([right, left, both], specs)):
    bidang_z(ax[row, 0], [0.5, 1], [0], inner=inner, outer=outer,
              limit=1.5, title='ROC: '+title)
    ax[row, 0].text(0.1, -0.18, '2', color=JINGGA, fontsize=10)
    stem(ax[row, 1], n, values)
    ax[row, 1].set_title('Invers untuk ROC '+title)
simpan(fig, '08_tiga_roc.png')
X = lambda z: 1/(1-1.5/z+0.5/z**2)
nr, nl = np.arange(200), -np.arange(1, 201)
z = 1.6*np.exp(0.2j)
cocok(zt(2-0.5**nr, nr, z), X(z))
z = 0.25*np.exp(0.2j)
cocok(zt(-2+0.5**nl, nl, z), X(z))
z = 0.75*np.exp(0.2j)
cocok(zt(np.full(len(nl), -2), nl, z)+zt(-0.5**nr, nr, z), X(z))
print('Ketiga invers memberikan fungsi rasional sama di dalam ROC masing-masing.')
