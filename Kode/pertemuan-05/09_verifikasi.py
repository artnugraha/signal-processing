"""Verifikasi seluruh sifat yang digunakan, pada blok real dan kompleks."""
from fourier import *

rng = np.random.default_rng(20261014)
for N in [3, 4, 5, 8, 9, 16]:
    x = rng.normal(size=N)+1j*rng.normal(size=N)
    h = rng.normal(size=N)+1j*rng.normal(size=N)
    X, H = np.fft.fft(x), np.fft.fft(h)
    n = np.arange(N)
    balik = (-n) % N
    cocok(dft(x), X)
    cocok(dft_matriks(x), X)
    cocok(idft(X), x)
    cocok(ifft_dengan_fft(X), x)
    cocok(np.fft.fft((2+1j)*x-0.3*h), (2+1j)*X-0.3*H)
    cocok(np.fft.fft(np.roll(x, 2)), np.exp(-2j*np.pi*n*2/N)*X)
    cocok(np.fft.fft(np.exp(2j*np.pi*2*n/N)*x), np.roll(X, 2))
    cocok(np.fft.fft(X), N*x[balik])
    cocok(np.fft.fft(konvolusi_siklik(x, h)), X*H)
    cocok(np.fft.fft(x*h), konvolusi_siklik(X, H)/N)
    cocok(np.fft.fft(x.conj()), X[balik].conj())
    cocok(np.fft.fft(x[balik].conj()), X.conj())
    cocok(np.fft.fft(x.real), (X+X[balik].conj())/2)
    cocok(np.fft.fft(1j*x.imag), (X-X[balik].conj())/2)
    cocok(np.fft.fft((x+x[balik].conj())/2), X.real)
    cocok(np.fft.fft((x-x[balik].conj())/2), 1j*X.imag)
    cocok(np.sum(abs(x)**2), np.sum(abs(X)**2)/N)
    xr = rng.normal(size=N)
    Xr = np.fft.fft(xr)
    cocok(Xr, Xr[balik].conj())
    cocok(np.fft.fft((xr+xr[balik])/2), Xr.real)
    cocok(np.fft.fft((xr-xr[balik])/2), 1j*Xr.imag)
    if (N & (N-1)) == 0:
        cocok(fft_dit(x), X)
        cocok(fft_dit_tahap(x)[0], X)
        cocok(fft_dif(x), X)
    print(f"N={N}: semua sifat DFT, simetri, invers, dan Parseval sesuai.")
for N in [0, 3, 6]:
    try:
        fft_dit(np.zeros(N))
    except ValueError:
        pass
    else:
        raise AssertionError("FFT radix-2 seharusnya menolak panjang ini.")
print("Validasi panjang radix-2 sesuai.")
print("Seluruh pemeriksaan matematis berhasil.")
