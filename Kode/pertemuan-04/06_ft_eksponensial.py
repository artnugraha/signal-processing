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

a=2.;w=np.linspace(-15,15,301);t=np.linspace(0,10,20001)
X=1/(a+1j*w)
# Integrasi trapezoidal dengan bobot eksplisit agar kompatibel lintas versi NumPy.
weights=np.full(len(t),t[1]-t[0]);weights[[0,-1]]*=.5
Xnum=np.exp(-1j*np.outer(w,t))@(weights*np.exp(-a*t))
err=np.max(np.abs(X-Xnum));assert err<1e-6
fig,ax=plt.subplots(2,1,figsize=(9,6))
ax[0].plot(w,np.abs(X),label='Analitik');ax[0].plot(w,np.abs(Xnum),'--',label='Numerik');ax[0].legend();ax[0].set(ylabel='Magnitudo (s)')
ax[1].plot(w,np.angle(X));ax[1].set(ylabel='Fase (rad)')
for aplot in ax:aplot.set_xlabel(r'$\omega$ (rad/s)')
save(fig,'06_ft_eksponensial');print('FT numerik: galat maksimum',err)
