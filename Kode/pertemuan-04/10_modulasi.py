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

a=.8;wc=np.pi/2;w=np.linspace(-np.pi,np.pi,1601)
X=lambda v:1/(1-a*np.exp(-1j*v))
Y=X(w-wc);Z=.5*(X(w-wc)+X(w+wc))
n=np.arange(120);x=a**n
assert np.max(np.abs(dtft(x*np.exp(1j*wc*n),n,w)-Y))<1e-10
assert np.max(np.abs(dtft(x*np.cos(wc*n),n,w)-Z))<1e-10
fig,ax=plt.subplots(3,1,figsize=(9,8))
for ar,z,title in zip(ax,[X(w),Y,Z],['Asli','Modulasi kompleks','Modulasi kosinus']):
    ar.plot(w/np.pi,np.abs(z));ar.set(title=title,xlabel=r'$\Omega/\pi$',ylabel='Magnitudo')
save(fig,'10_modulasi')
