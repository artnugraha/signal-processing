"""FFT delapan titik, nilai tiap tahap, dan hitungan operasi."""
from fourier import *

x = np.array([1, -1, -1, -1, 1, 1, 1, -1])
X, tahap = fft_dit_tahap(x)
cocok(X, dft(x))
cocok(X, fft_dit(x))
cocok(X, np.fft.fft(x))
expected = [
    [1, 1, -1, 1, -1, 1, -1, -1],
    [2, 0, 0, -2, 0, -2, -2, 0],
    [2, 2j, 2, -2j, -2, -2, 2, -2],
]
for i, values in enumerate(expected):
    cocok(tahap[i], values)
for i, values in enumerate(tahap):
    cetak(f"Tahap {i} =", values)

fig, ax = plt.subplots(figsize=(12, 7), layout="constrained")
ax.axis("off")
ax.set_xlim(-0.5, 3.55)
ax.set_ylim(-0.7, 8.1)
names = ["Masukan bit terbalik", "Tahap 1: dua titik", "Tahap 2: empat titik",
         "Tahap 3: delapan titik"]
for col in range(4):
    ax.text(col, 7.8, names[col], ha="center", fontsize=11, fontweight="bold")
    for row in range(8):
        ax.plot(col, 7-row, "o", color=BIRU, markersize=7)
        label = f"x[{indeks_bit_terbalik(8)[row]}]" if col == 0 else f"a{col}[{row}]"
        if col == 3:
            label = f"X[{row}]"
        ax.text(col+0.04, 7-row+0.13, label, fontsize=10, zorder=5,
                bbox=dict(facecolor="white", edgecolor="none", pad=0.3))
    if col:
        half = 2**(col-1)
        size = 2*half
        for start in range(0, 8, size):
            for r in range(half):
                p, q = start+r, start+r+half
                for source, dest in [(p, p), (p, q), (q, p), (q, q)]:
                    ax.annotate("", xy=(col-0.03, 7-dest), xytext=(col-1+0.03, 7-source),
                                arrowprops=dict(arrowstyle="->", linewidth=0.9,
                                                color=BIRU if source == dest else "#999999"),
                                zorder=0)
ax.text(1.5, -0.55, "Bobot butterfly dan nilai tiap tahap diberikan pada tabel serta keluaran program.",
        ha="center", fontsize=10)
simpan(fig, "07_fft_tahap.png")

N = 2**np.arange(2, 13)
fig, ax = plt.subplots(figsize=(8, 5), layout="constrained")
ax.loglog(N, N*N, "o-", color=JINGGA, label=r"DFT: $N^2$")
ax.loglog(N, N*np.log2(N)/2, "s-", color=BIRU, label=r"FFT: $(N/2)\log_2N$")
ax.set(xlabel="Jumlah titik N", ylabel="Jumlah perkalian kompleks",
       title="Hitungan dasar, termasuk perkalian dengan faktor sederhana")
ax.grid(alpha=0.25, which="both")
ax.legend()
simpan(fig, "08_jumlah_operasi.png")
print("N, perkalian DFT, penjumlahan DFT, perkalian FFT, penjumlahan FFT")
for n in [4, 8, 16, 64, 256, 1024]:
    v = n.bit_length()-1
    print(n, n*n, n*(n-1), n*v//2, n*v)
