"""Sampel DTFT, DFT empat titik, dan penambahan nol."""
from fourier import *

x = np.array([1, 0, 0, 1])
omega = np.linspace(0, 2*np.pi, 2001)
Xc = dtft(x, omega)
fig, ax = plt.subplots(2, 1, figsize=(9, 6), layout="constrained")
for panel, N in zip(ax, [4, 16]):
    wk = 2*np.pi*np.arange(N)/N
    X = np.fft.fft(x, N)
    cocok(X, dtft(x, wk))
    panel.plot(omega/np.pi, abs(Xc), color=BIRU, label="Magnitudo DTFT")
    marker, _, _ = panel.stem(wk/np.pi, abs(X))
    plt.setp(marker, color=JINGGA)
    marker.set_label(f"DFT {N} titik")
    panel.set(xlabel=r"Frekuensi $\Omega/\pi$", ylabel="Magnitudo",
              title=f"Blok yang sama, kisi frekuensi {N} titik")
    panel.legend()
    panel.grid(alpha=0.2)
    cetak(f"DFT {N} titik =", X)
simpan(fig, "01_dft_dtft.png")
print("Semua bin DFT sesuai dengan sampel DTFT blok asli.")
