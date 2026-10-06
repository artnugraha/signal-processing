"""Demo Kuliah 4. Jalankan: python NAMA_BERKAS.py. Memerlukan NumPy dan Matplotlib."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[2] / 'Gambar' / 'pertemuan-04'
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.size': 11, 'axes.grid': True,
                     'grid.alpha': 0.25, 'figure.dpi': 110})

def save(fig, name):
    fig.tight_layout()
    for ext in ('png', 'svg'):
        fig.savefig(OUT / f'{name}.{ext}', dpi=170)
    plt.close(fig)

def dtft(x, n, w):
    return np.exp(-1j*np.outer(w, n)) @ np.asarray(x)

def phase(z, tol=1e-10):
    out = np.angle(z)
    out[np.abs(z) < tol] = np.nan
    return out

x=np.array([1,2]);h=np.array([1,-1]);y=np.convolve(x,h)
assert np.array_equal(y,[1,1,-2])
w=np.linspace(-np.pi,np.pi,1001)
X=dtft(x,np.arange(len(x)),w);H=dtft(h,np.arange(len(h)),w);Y=dtft(y,np.arange(len(y)),w)
assert np.allclose(Y,X*H)
fig,ax=plt.subplots(2,2,figsize=(10,7))
for ar,z,title in zip(ax.flat[:3],[x,h,y],['x[n]','h[n]','y[n]']):
    ar.stem(np.arange(len(z)),z);ar.set(title=title,xlabel='n')
ax[1,1].plot(w/np.pi,np.abs(Y),label='DTFT y');ax[1,1].plot(w/np.pi,np.abs(X*H),'--',label='X H');ax[1,1].legend();ax[1,1].set(xlabel=r'$\Omega/\pi$',ylabel='Magnitudo')
save(fig,'11_konvolusi');print('Konvolusi: galat maksimum',np.max(np.abs(Y-X*H)))
