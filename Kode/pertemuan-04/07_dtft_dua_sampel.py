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

w=np.linspace(-2*np.pi,2*np.pi,1601);X=dtft([1,1],[0,1],w)
assert np.allclose(X,2*np.exp(-1j*w/2)*np.cos(w/2))
assert np.allclose(X,dtft([1,1],[0,1],w+2*np.pi))
fig,ax=plt.subplots(2,1,figsize=(9,6))
ax[0].plot(w/np.pi,np.abs(X));ax[0].set(ylabel='Magnitudo')
ax[1].plot(w/np.pi,phase(X));ax[1].set(ylabel='Fase utama (rad)')
for a in ax:a.set_xlabel(r'$\Omega/\pi$')
save(fig,'07_dtft_dua_sampel')
