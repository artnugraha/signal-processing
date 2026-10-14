"""Pergeseran siklik dan faktor perubahan fase DFT."""
from fourier import *

x = np.arange(6)
X = dft(x)
fig, ax = plt.subplots(3, 1, figsize=(8, 7), layout="constrained")
for panel, n0 in zip(ax, [0, 1, 4]):
    y = np.roll(x, n0)
    Y = dft(y)
    faktor = np.exp(-2j*np.pi*np.arange(6)*n0/6)
    cocok(Y, faktor*X)
    cocok(abs(Y), abs(X))
    stem(panel, np.arange(6), y)
    panel.set(title=f"Pergeseran siklik ke kanan {n0} sampel",
              xlabel="Indeks n", ylabel="Amplitudo")
    panel.set_xticks(np.arange(6))
    panel.set_ylim(-0.3, 5.8)
    cetak(f"n0={n0}, y =", y)
simpan(fig, "03_pergeseran_siklik.png")
print("Pergeseran mempertahankan magnitudo DFT.")
