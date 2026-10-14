"""Dua contoh DFT empat titik, magnitudo, dan fase."""
from fourier import *

x = np.array([1, 0, 0, 1])
X = dft(x)
cocok(X, [2, 1+1j, 0, 1-1j])
cocok(X, np.fft.fft(x))
fase = np.angle(X)
fase[abs(X) < 1e-12] = np.nan
fig, ax = plt.subplots(3, 1, figsize=(8, 7), layout="constrained")
stem(ax[0], np.arange(4), x)
ax[0].set(title="Contoh 1: sampel waktu", xlabel="Indeks n", ylabel="Amplitudo")
stem(ax[1], np.arange(4), abs(X))
ax[1].set(title="Magnitudo DFT", xlabel="Indeks k", ylabel="Magnitudo")
stem(ax[2], np.arange(4), fase/np.pi)
ax[2].text(2, 0.22, "Fase tidak\nterdefinisi", ha="center", fontsize=10)
ax[2].set(title="Fase pada bin yang tidak nol", xlabel="Indeks k",
          ylabel=r"Fase / $\pi$", ylim=(-0.4, 0.4))
for panel in ax:
    panel.set_xticks(np.arange(4))
simpan(fig, "02_dft_empat.png")
cetak("Contoh 1, X =", X)
cetak("Fase (radian) =", fase)
x2 = np.array([0, 1, 2, 3])
cocok(dft_matriks(x2), [6, -2+2j, -2, -2-2j])
cetak("Contoh 2, DFT matriks =", dft_matriks(x2))
N = len(x2)
D = np.exp(-2j*np.pi*np.arange(N)[:, None]*np.arange(N)[None, :]/N)
cocok(D.conj().T @ D, N*np.eye(N))
print("Ortogonalitas matriks DFT diperiksa.")
