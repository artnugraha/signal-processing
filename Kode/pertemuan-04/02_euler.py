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

theta=np.linspace(0,2*np.pi,500);phi=np.pi/3
fig,ax=plt.subplots(1,2,figsize=(10,4.4))
ax[0].plot(np.cos(theta),np.sin(theta));ax[0].arrow(0,0,np.cos(phi),np.sin(phi),length_includes_head=True,head_width=.06,color='tab:orange')
ax[0].plot([np.cos(phi),np.cos(phi)],[0,np.sin(phi)],'--');ax[0].plot([0,np.cos(phi)],[np.sin(phi),np.sin(phi)],'--')
ax[0].set(aspect='equal',xlabel='Bagian real',ylabel='Bagian imajiner',title='Lingkaran satuan',xlim=(-1.2,1.2),ylim=(-1.2,1.2))
ax[1].plot(theta,np.cos(theta),label='cos');ax[1].plot(theta,np.sin(theta),label='sin');ax[1].legend();ax[1].set(xlabel=r'$	heta$ (rad)',ylabel='Proyeksi')
save(fig,'02_euler')
