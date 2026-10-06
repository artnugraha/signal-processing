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

a=.5;N=30;n=np.arange(N);w=np.linspace(-2*np.pi,2*np.pi,1601)
X=1/(1-a*np.exp(-1j*w));Xn=dtft(a**n,n,w)
err=np.max(np.abs(X-Xn));bound=a**N/(1-a)
assert err<=bound+1e-14
# Verifikasi invers DTFT dari barisan berhingga memakai satu periode tanpa endpoint ganda.
wi=np.linspace(-np.pi,np.pi,512,endpoint=False)
back=np.exp(1j*np.outer(n,wi))@dtft(a**n,n,wi)/len(wi)
assert np.allclose(back,a**n,atol=1e-12)
fig,ax=plt.subplots(2,1,figsize=(9,6))
ax[0].plot(w/np.pi,np.abs(X),label='Analitik');ax[0].plot(w/np.pi,np.abs(Xn),'--',label=f'N={N}');ax[0].legend();ax[0].set(ylabel='Magnitudo')
ax[1].plot(w/np.pi,np.angle(X));ax[1].set(ylabel='Fase (rad)')
for ar in ax:ar.set_xlabel(r'$\Omega/\pi$')
save(fig,'08_dtft_eksponensial');print('DTFT: galat',err,'batas',bound)
