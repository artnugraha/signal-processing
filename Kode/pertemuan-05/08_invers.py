"""IDFT langsung dan IFFT melalui dua konjugasi."""
from fourier import *

fig, ax = plt.subplots(2, 1, figsize=(9, 6), layout="constrained")
for panel, x in zip(ax, [[1, 0, 0, 1], [1, -1, -1, -1, 1, 1, 1, -1]]):
    x = np.asarray(x)
    X = dft(x)
    langsung = idft(X)
    balik = ifft_dengan_fft(X, fft_dit)
    cocok(langsung, x)
    cocok(balik, x)
    cocok(balik, np.fft.ifft(X))
    stem(panel, np.arange(len(x)), langsung.real, BIRU, "IDFT")
    panel.plot(np.arange(len(x)), balik.real, "x", color=JINGGA,
               markersize=10, label="IFFT melalui FFT")
    panel.set(title=f"Rekonstruksi {len(x)} sampel", xlabel="Indeks n", ylabel="Amplitudo")
    panel.set_xticks(np.arange(len(x)))
    panel.set_ylim(-1.4, 1.4)
    panel.legend()
    cetak(f"IDFT {len(x)} titik =", langsung)
    print("Galat maksimum IFFT =", np.max(abs(balik-x)))
simpan(fig, "09_invers.png")
Y = [0, 4, 0, 0]
y = idft(Y)
cocok(y, [1, 1j, -1, -1j])
cetak("Invers spektrum kompleks Y =", y)
