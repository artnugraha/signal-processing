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

w=np.linspace(-np.pi,np.pi,1001);H=.5*(1+np.exp(-1j*w))
n=np.arange(24);x=2*np.cos(np.pi*n/2)
y=.5*(x+2*np.cos(np.pi*(n-1)/2));ys=np.sqrt(2)*np.cos(np.pi*n/2-np.pi/4)
assert np.allclose(y,ys,atol=1e-13)
# Respons rekursif dengan awal nol dan respons keadaan tunak.
r=np.empty(len(n));prev=0.
for i in n:
    r[i]=.5*prev+x[i];prev=r[i]
hr=1/(1-.5*np.exp(-1j*np.pi/2))
rsteady=2*np.abs(hr)*np.cos(np.pi*n/2+np.angle(hr))
diff=r-rsteady
assert np.allclose(diff[1:],.5*diff[:-1],atol=1e-13)
fig,ax=plt.subplots(2,2,figsize=(11,7))
ax[0,0].plot(w/np.pi,np.abs(H));ax[0,0].set(xlabel=r'$\Omega/\pi$',ylabel='Magnitudo H',title='Filter rata-rata dua sampel')
ax[0,1].plot(w/np.pi,phase(H));ax[0,1].set(xlabel=r'$\Omega/\pi$',ylabel='Fase H (rad)')
ax[1,0].plot(n,x,'o-',label='Masukan');ax[1,0].plot(n,y,'s-',label='Keluaran');ax[1,0].legend();ax[1,0].set(xlabel='n',title='Rata-rata: sinusoid sepanjang waktu')
ax[1,1].plot(n,r,'o-',label='Awal nol');ax[1,1].plot(n,rsteady,'--',label='Keadaan tunak');ax[1,1].legend();ax[1,1].set(xlabel='n',title='Sistem rekursif: transien')
save(fig,'12_lti');print('LTI: sinusoid dan transien lolos')
