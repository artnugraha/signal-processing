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

w=np.linspace(-.99*np.pi,.99*np.pi,1001)
X=dtft([1,1],[0,1],w);Y=dtft([1,1],[3,4],w)
assert np.allclose(Y,np.exp(-3j*w)*X)
fig,ax=plt.subplots(2,1,figsize=(9,6))
ax[0].plot(w/np.pi,np.abs(X),label='Asli');ax[0].plot(w/np.pi,np.abs(Y),'--',label='Tertunda 3 sampel');ax[0].legend();ax[0].set(ylabel='Magnitudo')
ax[1].plot(w/np.pi,-w/2,label='Fase asli');ax[1].plot(w/np.pi,-3.5*w,label='Fase tertunda');ax[1].legend();ax[1].set(ylabel='Fase kontinu (rad)')
for ar in ax:ar.set_xlabel(r'$\Omega/\pi$')
save(fig,'09_pergeseran')
