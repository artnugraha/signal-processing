"""Fungsi pembelajaran transformasi Z; hanya membutuhkan NumPy dan Matplotlib."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

ROOT = Path(__file__).resolve().parents[2]
GAMBAR = ROOT / 'Gambar' / 'pertemuan-06'
BIRU = '#176b9a'
JINGGA = '#cd641e'
plt.rcParams.update({'font.size': 10.5, 'axes.titlesize': 11,
                     'axes.grid': True, 'grid.alpha': 0.2})


def zt(x, n, z):
    """Jumlah transformasi sampel berhingga, dengan indeks eksplisit."""
    x = np.asarray(x, dtype=complex)
    n = np.asarray(n, dtype=int)
    z = np.asarray(z, dtype=complex)
    if x.ndim != 1 or x.shape != n.shape:
        raise ValueError('Nilai sampel dan indeks harus berupa vektor yang sama panjang.')
    return np.sum(x*z[..., None]**(-n), axis=-1)


def zplus(x, n, z):
    x, n = np.asarray(x), np.asarray(n)
    keep = n >= 0
    return zt(x[keep], n[keep], z)


def deret_rasional(b, a, jumlah):
    """Koefisien B(q)/A(q), q=z**(-1), koefisien diurutkan dari q**0."""
    b, a = np.asarray(b, complex), np.asarray(a, complex)
    if not len(a) or a[0] == 0:
        raise ValueError('Koefisien konstanta penyebut harus tidak nol.')
    c = np.zeros(jumlah, dtype=complex)
    for m in range(jumlah):
        rhs = b[m] if m < len(b) else 0
        for k in range(1, min(m, len(a)-1)+1):
            rhs -= a[k]*c[m-k]
        c[m] = rhs/a[0]
    return c


def invers_kontur(X, n, rho, M=1024):
    """Jumlah trapezoidal periodik pada lingkaran yang berada di ROC."""
    n = np.asarray(n, dtype=int)
    theta = 2*np.pi*np.arange(M)/M
    z = rho*np.exp(1j*theta)
    return rho**n*(np.exp(1j*np.outer(n, theta)) @ X(z))/M


def cocok(a, b, tol=1e-10):
    np.testing.assert_allclose(a, b, atol=tol, rtol=tol)


def stem(ax, n, x, warna=BIRU, label=None):
    marker, lines, baseline = ax.stem(n, np.real_if_close(x))
    plt.setp(marker, color=warna, markersize=5)
    plt.setp(lines, color=warna, linewidth=1.4)
    plt.setp(baseline, color='#777777', linewidth=0.6)
    if label:
        marker.set_label(label)
    ax.set_xlabel('Indeks n')
    ax.set_ylabel('Amplitudo')


def bidang_z(ax, poles=(), zeros=(), inner=0, outer=np.inf,
             limit=2.2, shade=True, title=''):
    """Gambar pole, zero, lingkaran satuan, dan ROC radial."""
    grid = np.linspace(-limit, limit, 301)
    xx, yy = np.meshgrid(grid, grid)
    radius = np.hypot(xx, yy)
    if shade:
        mask = ((radius > inner) & (radius < outer)).astype(float)
        ax.contourf(xx, yy, mask, levels=[0.5, 1.5], colors=['#b8dce9'], alpha=0.65)
    ax.add_patch(Circle((0, 0), 1, fill=False, linestyle='--', linewidth=1,
                        edgecolor='#888888', label='Lingkaran satuan'))
    for r in sorted(set([inner, outer])):
        if np.isfinite(r) and r > 0:
            ax.add_patch(Circle((0, 0), r, fill=False, linestyle=':',
                                edgecolor=BIRU, linewidth=1.5))
    if len(zeros):
        zz = np.asarray(zeros, complex)
        ax.scatter(zz.real, zz.imag, marker='o', facecolors='none',
                   edgecolors=JINGGA, s=75, linewidths=1.7, zorder=6, label='Zero')
    if len(poles):
        pp = np.asarray(poles, complex)
        ax.scatter(pp.real, pp.imag, marker='x', color='#b52d2d',
                   s=80, linewidths=2, zorder=7, label='Pole')
    ax.axhline(0, color='#777777', linewidth=0.6)
    ax.axvline(0, color='#777777', linewidth=0.6)
    ax.set(aspect='equal', xlim=(-limit, limit), ylim=(-limit, limit),
           xlabel='Bagian real z', ylabel='Bagian imajiner z', title=title)


def simpan(fig, nama):
    GAMBAR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(GAMBAR/nama, dpi=170, bbox_inches='tight')
    plt.close(fig)


def cetak(nama, data):
    print(nama, np.round(np.asarray(data), 8))
