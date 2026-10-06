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

t=np.linspace(-1,1,4001);D=.5
x=(np.abs((t+.5)%1-.5)<D/2).astype(float)
fig,ax=plt.subplots(2,1,figsize=(10,7))
ax[0].plot(t,x,'k--',label='Pulsa ideal')
for K in [3,15,60]:
    k=np.arange(-K,K+1);C=D*np.sinc(k*D)
    s=np.exp(1j*2*np.pi*np.outer(t,k))@C
    assert np.max(np.abs(s.imag))<1e-12
    ax[0].plot(t,s.real,label=f'K={K}')
ax[0].legend(ncol=4);ax[0].set(xlabel='t / T0',ylabel='Amplitudo',ylim=(-.2,1.3))
k=np.arange(-15,16);ax[1].stem(k,D*np.sinc(k*D));ax[1].set(xlabel='k',ylabel='Koefisien bertanda Ck')
save(fig,'04_fs_pulsa')
