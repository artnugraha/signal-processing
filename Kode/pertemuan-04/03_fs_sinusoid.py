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

k=np.arange(-2,3);C=np.array([.5j,1,1,1,-.5j])
t=np.linspace(0,1,1001);w0=2*np.pi
s=np.exp(1j*np.outer(t*w0,k))@C
x=1+2*np.cos(w0*t)+np.sin(2*w0*t)
assert np.max(np.abs(s-x))<1e-12
assert np.isclose(np.sum(np.abs(C)**2),3.5)
fig,ax=plt.subplots(3,1,figsize=(9,8))
ax[0].plot(t,x,label='Rumus real');ax[0].plot(t,s.real,'--',label='Sintesis FS');ax[0].legend();ax[0].set(xlabel='t (s)',ylabel='x(t)')
ax[1].stem(k,np.abs(C));ax[1].set(ylabel='Magnitudo koefisien',xlabel='k')
ax[2].stem(k,np.angle(C));ax[2].set(ylabel='Fase (rad)',xlabel='k')
save(fig,'03_fs_sinusoid')
print('FS: galat maksimum',np.max(np.abs(s-x)))
