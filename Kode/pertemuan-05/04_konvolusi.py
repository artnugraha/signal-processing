"""Konvolusi linear melalui FFT dan contoh konvolusi siklik."""
from fourier import *

x = np.array([-2, 0, 1, -1, 3])
h = np.array([1, 2, 0, -1])
y = np.convolve(x, h)
cocok(y, [-2, -4, 1, 3, 1, 5, 1, -3])
X, H = np.fft.fft(x, 8), np.fft.fft(h, 8)
y8 = np.fft.ifft(X*H)
cocok(y8, y)
y5 = np.fft.ifft(np.fft.fft(x, 5)*np.fft.fft(h, 5))
cocok(y5, [3, -3, -2, 3, 1])
print("k : X[k], H[k], Y[k]")
for k in range(8):
    print(k, np.round(X[k], 4), np.round(H[k], 4), np.round(X[k]*H[k], 4))
cetak("Konvolusi linear =", y)
cetak("Konvolusi siklik N=5 =", y5)
fig, ax = plt.subplots(3, 1, figsize=(9, 7), layout="constrained")
for panel, values, title in zip(
    ax, [y, y8.real, y5.real],
    ["Konvolusi linear langsung", "FFT/IFFT delapan titik: tanpa pelipatan",
     "FFT/IFFT lima titik: sampel akhir terlipat ke awal"]
):
    stem(panel, np.arange(len(values)), values)
    panel.set(title=title, xlabel="Indeks n", ylabel="Amplitudo", ylim=(-5, 6))
    panel.set_xticks(np.arange(len(values)))
simpan(fig, "04_konvolusi.png")
xc, hc = np.array([1, 2, 3, 0]), np.array([2, 1, 0, 0])
yc = konvolusi_siklik(xc, hc)
cocok(yc, [2, 5, 8, 3])
cocok(yc, np.fft.ifft(np.fft.fft(xc)*np.fft.fft(hc)))
cetak("Contoh 5, hasil siklik =", yc)
