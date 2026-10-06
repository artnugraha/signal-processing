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

w=np.linspace(-8*np.pi,8*np.pi,2001);X=np.sinc(w/(2*np.pi))
fig,ax=plt.subplots(3,1,figsize=(9,8))
ax[0].plot(w,X);ax[0].set(ylabel='X bertanda (s)',title='Pulsa A=1, lebar 1 s')
ax[1].plot(w,np.abs(X));ax[1].set(ylabel='Magnitudo (s)')
ax[2].plot(w,phase(X.astype(complex)));ax[2].set(ylabel='Fase (rad)')
for a in ax:a.set_xlabel(r'$\omega$ (rad/s)')
assert np.isclose(X[len(w)//2],1)
save(fig,'05_ft_pulsa')
