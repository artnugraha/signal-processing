"""Fungsi pembelajaran DFT, IDFT, FFT radix-2, dan konvolusi siklik."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
GAMBAR = ROOT / "Gambar" / "pertemuan-05"
BIRU = "#176b9a"
JINGGA = "#cf6a20"
plt.rcParams.update({"font.size": 11, "axes.titlesize": 12})


def blok(x):
    x = np.asarray(x, dtype=complex)
    if x.ndim != 1 or len(x) == 0:
        raise ValueError("Masukan harus berupa blok satu dimensi yang tidak kosong.")
    return x


def dft(x):
    x = blok(x)
    N = len(x)
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        for n in range(N):
            X[k] += x[n]*np.exp(-2j*np.pi*k*n/N)
    return X


def dft_matriks(x):
    x = blok(x)
    N = len(x)
    k = np.arange(N)[:, None]
    n = np.arange(N)[None, :]
    return np.exp(-2j*np.pi*k*n/N) @ x


def idft(X):
    X = blok(X)
    N = len(X)
    x = np.zeros(N, dtype=complex)
    for n in range(N):
        for k in range(N):
            x[n] += X[k]*np.exp(2j*np.pi*k*n/N)/N
    return x


def dtft(x, omega):
    x = blok(x)
    omega = np.asarray(omega)
    return np.exp(-1j*omega[..., None]*np.arange(len(x))) @ x


def pangkat_dua(N):
    if N < 1 or (N & (N-1)) != 0:
        raise ValueError("Panjang harus berupa pangkat dua positif.")


def indeks_bit_terbalik(N):
    pangkat_dua(N)
    if N == 1:
        return np.array([0])
    v = N.bit_length()-1
    return np.array([int(format(n, f"0{v}b")[::-1], 2) for n in range(N)])


def fft_dit(x):
    x = blok(x)
    N = len(x)
    pangkat_dua(N)
    if N == 1:
        return x.copy()
    E = fft_dit(x[::2])
    O = fft_dit(x[1::2])
    W = np.exp(-2j*np.pi*np.arange(N//2)/N)
    T = W*O
    return np.concatenate((E+T, E-T))


def fft_dit_tahap(x):
    """Kembalikan DFT dalam urutan biasa dan daftar nilai pada tiap tahap."""
    x = blok(x)
    N = len(x)
    a = x[indeks_bit_terbalik(N)].copy()
    tahap = [a.copy()]
    ukuran = 2
    while ukuran <= N:
        separuh = ukuran//2
        for awal in range(0, N, ukuran):
            for r in range(separuh):
                w = np.exp(-2j*np.pi*r/ukuran)
                p = awal+r
                q = p+separuh
                u = a[p]
                t = w*a[q]
                a[p] = u+t
                a[q] = u-t
        tahap.append(a.copy())
        ukuran *= 2
    return a, tahap


def fft_dif_tahap(x):
    """Kembalikan keluaran DIF mentah (bit terbalik) dan tiap tahap."""
    x = blok(x)
    N = len(x)
    pangkat_dua(N)
    a = x.copy()
    tahap = [a.copy()]
    ukuran = N
    while ukuran >= 2:
        separuh = ukuran//2
        for awal in range(0, N, ukuran):
            for r in range(separuh):
                w = np.exp(-2j*np.pi*r/ukuran)
                p = awal+r
                q = p+separuh
                u, v = a[p], a[q]
                a[p] = u+v
                a[q] = (u-v)*w
        tahap.append(a.copy())
        ukuran //= 2
    return a, tahap


def fft_dif(x):
    mentah, _ = fft_dif_tahap(x)
    return mentah[indeks_bit_terbalik(len(mentah))]


def ifft_dengan_fft(X, fungsi_fft=np.fft.fft):
    X = blok(X)
    return np.conj(fungsi_fft(np.conj(X)))/len(X)


def konvolusi_siklik(x, h):
    x, h = blok(x), blok(h)
    if len(x) != len(h):
        raise ValueError("Kedua blok harus mempunyai panjang yang sama.")
    N = len(x)
    y = np.zeros(N, dtype=complex)
    for n in range(N):
        for m in range(N):
            y[n] += x[m]*h[(n-m) % N]
    return y


def stem(ax, n, x, warna=BIRU, label=None):
    marker, lines, baseline = ax.stem(n, x)
    plt.setp(marker, color=warna, markersize=6)
    plt.setp(lines, color=warna, linewidth=1.6)
    plt.setp(baseline, color="#777777", linewidth=0.7)
    if label:
        marker.set_label(label)
    ax.grid(alpha=0.2)


def simpan(fig, nama):
    GAMBAR.mkdir(parents=True, exist_ok=True)
    fig.savefig(GAMBAR/nama, dpi=180, bbox_inches="tight")
    plt.close(fig)


def cocok(a, b):
    np.testing.assert_allclose(a, b, atol=1e-10, rtol=1e-10)


def cetak(nama, x, digit=4):
    print(nama, np.round(np.asarray(x), digit))
