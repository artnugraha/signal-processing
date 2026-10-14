"""Ilustrasi spektrum empat representasi dengan normalisasi masing-masing."""
from fourier import *

fig, ax = plt.subplots(2, 2, figsize=(11, 7), layout="constrained")
k = np.arange(-10, 11)
# Pulsa tinggi 1, lebar 1, perioda 4: Ck = (1/4) sinc(k/4).
stem(ax[0, 0], k, abs(0.25*np.sinc(k/4)))
ax[0, 0].set(title="FS: harmonik diskret, tidak harus periodik",
             xlabel="Indeks harmonik k", ylabel=r"$|C_k|$")
omega = np.linspace(-8*np.pi, 8*np.pi, 1201)
# Pulsa tunggal tinggi 1, lebar 1: X(w) = sinc(w/(2 pi)).
ax[0, 1].plot(omega/np.pi, abs(np.sinc(omega/(2*np.pi))), color=BIRU)
ax[0, 1].set(title="FT: variabel kontinu, tidak wajib periodik",
             xlabel=r"Frekuensi $\omega/\pi$ (rad/s dibagi $\pi$)", ylabel=r"$|X(\omega)|$")
Omega = np.linspace(-2*np.pi, 4*np.pi, 1801)
ax[1, 0].plot(Omega/np.pi, abs(dtft([1, 0, 0, 1], Omega)), color=BIRU)
ax[1, 0].set(title=r"DTFT: kontinu dan periodik $2\pi$",
             xlabel=r"Frekuensi $\Omega/\pi$", ylabel=r"$|X(e^{j\Omega})|$")
kk = np.arange(-4, 12)
X = np.fft.fft([1, 0, 0, 1])
stem(ax[1, 1], kk, abs(X[kk % 4]))
ax[1, 1].set(title="DFT: bin diskret dan periodik N=4",
             xlabel="Indeks frekuensi k", ylabel=r"$|X[k]|$")
for panel in ax.ravel():
    panel.grid(alpha=0.2)
simpan(fig, "10_representasi.png")
print("FS dan FT: pulsa lebar 1; DTFT dan DFT: blok {1,0,0,1}.")
