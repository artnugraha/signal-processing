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

t=np.linspace(0,1,2001)
x1=np.cos(2*np.pi*3*t)
x2=.4*np.cos(2*np.pi*12*t+np.pi/3)
fig,ax=plt.subplots(3,1,figsize=(9,8))
ax[0].plot(t,x1,label='3 Hz');ax[0].plot(t,x2,label='12 Hz');ax[0].legend()
ax[1].plot(t,x1+x2);ax[1].set_title('Sinyal campuran')
ax[2].stem([3,12],[1,.4]);ax[2].set(xlabel='Frekuensi (Hz)',ylabel='Amplitudo kosinus',xlim=(0,15),title='Spektrum satu sisi analitik')
for a in ax[:2]:a.set(xlabel='t (s)',ylabel='Amplitudo')
save(fig,'01_motivasi')
