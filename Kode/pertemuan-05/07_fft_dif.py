"""FFT DIF, keluaran bit terbalik, dan penataan akhir."""
from fourier import *

x = [0, 1, 2, 3]
mentah, tahap = fft_dif_tahap(x)
for i, a in enumerate(tahap):
    cetak(f"Tahap DIF {i} =", a)
cetak("Keluaran mentah =", mentah)
X = mentah[indeks_bit_terbalik(4)]
cetak("Setelah penataan ulang =", X)
cocok(X, [6, -2+2j, -2, -2-2j])
cocok(X, fft_dit(x))
rng = np.random.default_rng(20261014)
for N in [1, 2, 4, 8, 16, 32]:
    x = rng.normal(size=N)+1j*rng.normal(size=N)
    cocok(fft_dif(x), np.fft.fft(x))
print("DIF dan FFT NumPy cocok untuk deret kompleks sampai 32 titik.")
