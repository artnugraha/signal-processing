"""Solusi latihan hitungan Pertemuan 5: pemeriksaan dan sepuluh gambar.

Jalankan: python Kode/solusi-kuliah-05/buat_gambar_solusi_05.py
Dependensi: numpy, matplotlib. Tidak memerlukan desktop atau berkas masukan.
Gambar disimpan relatif terhadap lokasi skrip, bukan lokasi terminal.
"""
from pathlib import Path
from io import BytesIO
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Gambar" / "solusi-kuliah-05"
OUT.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN = "#175c9a", "#ce641d", "#188479"
plt.rcParams.update({
    "font.size": 11, "figure.dpi": 110, "axes.titlesize": 12,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.18, "axes.titleweight": "bold",
})


def save(fig, number):
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=170, bbox_inches="tight", facecolor="white")
    (OUT / f"soal-{number:02d}.png").write_bytes(buf.getvalue())
    plt.close(fig)
    print(f"Gambar {number:02d} tersimpan.")


def stem(ax, n, y, color=BLUE, label=None, annotate=False):
    n, y = np.asarray(n), np.asarray(y)
    ax.vlines(n, 0, y, color=color, lw=1.7, alpha=0.8)
    ax.plot(n, y, "o", color=color, ms=5, label=label)
    ax.axhline(0, color="0.4", lw=0.7)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if annotate:
        for ni, yi in zip(n, y):
            value = 0.0 if abs(yi) < 1e-12 else yi
            ax.annotate(f"{value:g}", (ni, yi), xytext=(0, 8 if yi >= 0 else -15),
                        textcoords="offset points", ha="center", fontsize=10)
    ax.margins(x=0.08, y=0.25)


def complex_stem(ax, values):
    values = np.asarray(values)
    n = np.arange(len(values))
    stem(ax, n, values.real, BLUE, "Real")
    ax.vlines(n, 0, values.imag, color=ORANGE, lw=1.3, alpha=0.7)
    ax.plot(n, values.imag, "s", mfc="none", mec=ORANGE, ms=7, label="Imajiner")
    ax.legend(fontsize=9, loc="upper right")


def dft(x):
    """DFT melalui matriks eksponensial; tanda negatif, tanpa faktor 1/N."""
    x = np.asarray(x, dtype=complex)
    N = len(x)
    indices = np.arange(N)
    return np.exp(-2j*np.pi*np.outer(indices, indices)/N) @ x


def idft(X):
    """IDFT langsung; tanda positif dan faktor 1/N."""
    X = np.asarray(X, dtype=complex)
    N = len(X)
    indices = np.arange(N)
    return np.exp(2j*np.pi*np.outer(indices, indices)/N) @ X / N


def bit_reverse_indices(N):
    if N < 1 or (N & (N-1)) != 0:
        raise ValueError("Panjang radix-2 harus berupa pangkat dua positif.")
    width = (N-1).bit_length()
    return np.array([int(f"{i:0{width}b}"[::-1], 2) for i in range(N)])


def fft_dit_stages(x):
    """DIT iteratif: masukan bit terbalik, keluaran dalam urutan biasa."""
    x = np.asarray(x, dtype=complex)
    N = len(x)
    permutation = bit_reverse_indices(N)
    work = x[permutation].copy()
    stages = [work.copy()]
    L = 2
    while L <= N:
        for start in range(0, N, L):
            for r in range(L//2):
                left, right = start+r, start+r+L//2
                a, b = work[left], work[right]
                wb = np.exp(-2j*np.pi*r/L) * b
                work[left], work[right] = a+wb, a-wb
        stages.append(work.copy())
        L *= 2
    return work, stages, permutation


def fft_dif_stages(x):
    """DIF iteratif: keluaran mentah bit terbalik, kemudian ditata ulang."""
    work = np.asarray(x, dtype=complex).copy()
    N = len(work)
    permutation = bit_reverse_indices(N)
    stages = [work.copy()]
    L = N
    while L >= 2:
        for start in range(0, N, L):
            for r in range(L//2):
                left, right = start+r, start+r+L//2
                a, b = work[left], work[right]
                work[left] = a+b
                work[right] = (a-b) * np.exp(-2j*np.pi*r/L)
        stages.append(work.copy())
        L //= 2
    return work[permutation], work.copy(), stages, permutation


def phase_bins(X):
    phase = np.angle(X)
    phase[np.abs(X) < 1e-12] = np.nan
    return phase


# Soal 1: DFT empat titik, termasuk kuadran fase dan bin nol.
x1 = np.array([0, 1, 1, 0])
X1 = dft(x1)
np.testing.assert_allclose(X1, [2, -1-1j, 0, -1+1j], atol=1e-12)
np.testing.assert_allclose(X1, np.fft.fft(x1), atol=1e-12)
phase1 = phase_bins(X1)
np.testing.assert_allclose(phase1[[0, 1, 3]], [0, -3*np.pi/4, 3*np.pi/4], atol=1e-12)
assert np.isnan(phase1[2])
fig, ax = plt.subplots(3, 1, figsize=(10.5, 7), constrained_layout=True)
stem(ax[0], np.arange(4), x1, annotate=True)
ax[0].set(title="Soal 1: blok masukan", xlabel="Indeks n", ylabel="x[n]")
stem(ax[1], np.arange(4), np.abs(X1))
ax[1].set(title="Magnitudo DFT", xlabel="Bin k", ylabel="Magnitudo")
valid = np.isfinite(phase1)
stem(ax[2], np.arange(4)[valid], phase1[valid]/np.pi)
ax[2].set(title="Fase hanya pada bin tak nol; k = 2 tidak terdefinisi",
          xlabel="Bin k", ylabel="Fase / pi", xticks=range(4))
save(fig, 1)

# Soal 2: matriks, DC, rata-rata dan energi.
x2 = np.array([1, 2, 1, 0])
X2 = dft(x2)
np.testing.assert_allclose(X2, [4, -2j, 0, 2j], atol=1e-12)
energy2 = np.abs(X2)**2 / len(x2)
np.testing.assert_allclose(energy2.sum(), 6, atol=1e-12)
np.testing.assert_allclose(X2[0]/4, 1, atol=1e-12)
fig, ax = plt.subplots(3, 1, figsize=(10.5, 7), constrained_layout=True)
stem(ax[0], np.arange(4), x2, annotate=True)
ax[0].set(title="Soal 2: empat sampel dengan jumlah nilai empat", xlabel="Indeks n", ylabel="x[n]")
complex_stem(ax[1], X2)
ax[1].set(title="Hasil perkalian matriks DFT", xlabel="Bin k", ylabel="X[k]")
ax[2].bar(np.arange(4), energy2, color=BLUE, alpha=0.8)
ax[2].set(title="Kontribusi energi |X[k]| kuadrat / 4; jumlah = 6",
          xlabel="Bin k", ylabel="Kontribusi energi", xticks=range(4))
save(fig, 2)

# Soal 3: DFT sebagai sampel DTFT yang sama.
O3 = np.linspace(0, 2*np.pi, 2401)
DTFT3 = 1+np.exp(-1j*O3)
O2bins, O4bins = np.pi*np.arange(2), (np.pi/2)*np.arange(4)
DFT2, DFT4 = dft([1, 1]), dft([1, 1, 0, 0])
np.testing.assert_allclose(DFT2, [2, 0], atol=1e-12)
np.testing.assert_allclose(DFT4, [2, 1-1j, 0, 1+1j], atol=1e-12)
np.testing.assert_allclose(DFT4, 1+np.exp(-1j*O4bins), atol=1e-12)
fig, ax = plt.subplots(2, 1, figsize=(10.5, 6), sharex=True, constrained_layout=True)
for a, part, name in [(ax[0], np.real, "Bagian real"), (ax[1], np.imag, "Bagian imajiner")]:
    a.plot(O3/np.pi, part(DTFT3), color=BLUE, lw=2, label="DTFT kontinu")
    a.scatter(O2bins/np.pi, part(DFT2), s=120, facecolors="none", edgecolors=ORANGE,
              linewidths=2, label="DFT dua titik", zorder=4)
    a.plot(O4bins/np.pi, part(DFT4), "x", color=GREEN, ms=8, mew=2,
           label="DFT empat titik", zorder=5)
    a.set(ylabel=name, xlim=(-0.05, 2.05), xticks=[0, 0.5, 1, 1.5, 2])
ax[0].set_title("Soal 3: penambahan nol mengambil sampel DTFT lebih rapat")
ax[0].legend(fontsize=9, loc="lower right")
ax[1].set_xlabel(r"$\Omega/\pi$")
save(fig, 3)

# Soal 4: sifat pergeseran waktu dan frekuensi siklik.
x4 = np.array([1, 2, 3, 4])
k4 = np.arange(4)
X4 = dft(x4)
y4 = np.roll(x4, 1)
z4 = np.exp(1j*np.pi*k4/2)*x4
Y4 = np.exp(-1j*np.pi*k4/2)*X4
Z4 = np.roll(X4, 1)
np.testing.assert_allclose(X4, [10, -2+2j, -2, -2-2j], atol=1e-12)
np.testing.assert_array_equal(y4, [4, 1, 2, 3])
np.testing.assert_allclose(z4, [1, 2j, -3, -4j], atol=1e-12)
np.testing.assert_allclose(Y4, [10, 2+2j, 2, 2-2j], atol=1e-12)
np.testing.assert_allclose(Z4, [-2-2j, 10, -2+2j, -2], atol=1e-12)
np.testing.assert_allclose(dft(y4), Y4, atol=1e-12)
np.testing.assert_allclose(dft(z4), Z4, atol=1e-12)
fig, ax = plt.subplots(2, 2, figsize=(11, 6.2), constrained_layout=True)
stem(ax[0, 0], k4, x4, annotate=True)
ax[0, 0].set(title="Soal 4: x[n]", xlabel="Indeks n", ylabel="Amplitudo")
stem(ax[0, 1], k4, y4, ORANGE, annotate=True)
ax[0, 1].set(title="y[n]: geser siklik satu ke kanan", xlabel="Indeks n", ylabel="Amplitudo")
stem(ax[1, 0], k4, np.abs(X4), BLUE, "|X[k]|")
ax[1, 0].plot(k4, np.abs(Y4), "s", mfc="none", mec=ORANGE, ms=8, label="|Y[k]|")
ax[1, 0].set(title="Penundaan mempertahankan magnitudo", xlabel="Bin k", ylabel="Magnitudo")
ax[1, 0].legend(fontsize=9)
stem(ax[1, 1], k4, np.abs(Z4), GREEN)
ax[1, 1].set(title="Modulasi: |Z[k]| = |X[(k-1) mod 4]|", xlabel="Bin k", ylabel="Magnitudo")
save(fig, 4)

# Soal 5: konvolusi siklik, DFT/IDFT, dan hasil linear dengan ekor nol.
x5, h5 = np.array([1, 2, 0, 1]), np.array([1, -1, 0, 0])
yc5 = np.array([sum(x5[m]*h5[(n-m)%4] for m in range(4)) for n in range(4)])
X5, H5 = dft(x5), dft(h5)
Y5 = X5*H5
np.testing.assert_allclose(X5, [4, 1-1j, -2, 1+1j], atol=1e-12)
np.testing.assert_allclose(H5, [0, 1+1j, 2, 1-1j], atol=1e-12)
np.testing.assert_allclose(Y5, [0, 2, -4, 2], atol=1e-12)
np.testing.assert_array_equal(yc5, [0, 1, -2, 1])
np.testing.assert_allclose(idft(Y5), yc5, atol=1e-12)
linear5 = np.convolve(x5, h5)
np.testing.assert_array_equal(linear5, [1, 1, -2, 1, -1, 0, 0])
fold5 = np.zeros(4, dtype=int)
for n, value in enumerate(linear5):
    fold5[n%4] += value
np.testing.assert_array_equal(fold5, yc5)
fig, ax = plt.subplots(2, 2, figsize=(11, 6.2), constrained_layout=True)
for a, values, title, color in [
    (ax[0, 0], x5, "Soal 5: x[n]", BLUE), (ax[0, 1], h5, "h[n]", ORANGE),
    (ax[1, 0], linear5, "Linear: sampel pada n = 4 bernilai -1", BLUE),
    (ax[1, 1], yc5, "Siklik empat titik: y[0] = 1 + (-1) = 0", GREEN)]:
    stem(a, np.arange(len(values)), values, color, annotate=True)
    a.set(title=title, xlabel="Indeks n", ylabel="Amplitudo")
save(fig, 5)

# Soal 6: panjang minimum lima; radix-2 boleh memilih delapan.
x6, h6 = np.array([1, 2, 3]), np.array([1, 1, 1])
manual6 = np.array([1, 3, 6, 5, 3])
P6 = len(x6)+len(h6)-1
assert P6 == 5
yp5 = idft(dft(np.pad(x6, (0, 2)))*dft(np.pad(h6, (0, 2))))
yp8 = np.fft.ifft(np.fft.fft(x6, 8)*np.fft.fft(h6, 8))
np.testing.assert_array_equal(np.convolve(x6, h6), manual6)
np.testing.assert_allclose(yp5, manual6, atol=1e-12)
np.testing.assert_allclose(yp8, np.pad(manual6, (0, 3)), atol=1e-12)
fig = plt.figure(figsize=(11, 6.2), constrained_layout=True)
gs = fig.add_gridspec(2, 2)
for a, values, title in [(fig.add_subplot(gs[0, 0]), x6, "Soal 6: x[n]"),
                          (fig.add_subplot(gs[0, 1]), h6, "h[n]")]:
    stem(a, np.arange(3), values, annotate=True)
    a.set(title=title, xlabel="Indeks n", ylabel="Amplitudo")
a = fig.add_subplot(gs[1, :])
stem(a, np.arange(5), manual6, BLUE, "Hitungan manual")
a.plot(np.arange(5), yp5.real, "s", mfc="none", mec=ORANGE, ms=8, label="DFT/IDFT lima titik")
a.plot(np.arange(8), yp8.real, "x", color=GREEN, ms=7, label="FFT/IFFT delapan titik")
a.set(title="Seluruh hasil linear muat mulai panjang lima", xlabel="Indeks n", ylabel="y[n]")
a.legend(fontsize=9)
save(fig, 6)

# Soal 7: DIT delapan titik, seluruh tahap dibandingkan dengan hitungan manual.
x7 = np.array([1, 1, 1, 1, 0, 0, 0, 0])
X7, stages7, permutation7 = fft_dit_stages(x7)
s2 = np.sqrt(2)
expected7 = np.array([4, 1-1j*(1+s2), 0, 1-1j*(s2-1),
                      0, 1+1j*(s2-1), 0, 1+1j*(1+s2)])
np.testing.assert_array_equal(permutation7, [0, 4, 2, 6, 1, 5, 3, 7])
np.testing.assert_allclose(stages7[0], [1, 0, 1, 0, 1, 0, 1, 0], atol=1e-12)
np.testing.assert_allclose(stages7[1], np.ones(8), atol=1e-12)
np.testing.assert_allclose(stages7[2], [2, 1-1j, 0, 1+1j, 2, 1-1j, 0, 1+1j], atol=1e-12)
np.testing.assert_allclose(X7, expected7, atol=1e-12)
np.testing.assert_allclose(X7, dft(x7), atol=1e-12)
np.testing.assert_allclose(X7, np.fft.fft(x7), atol=1e-12)
np.testing.assert_allclose(X7[(-np.arange(8))%8], X7.conj(), atol=1e-12)
np.testing.assert_allclose(X7[0], x7.sum(), atol=1e-12)
fig, ax = plt.subplots(2, 2, figsize=(12, 7), constrained_layout=True)
titles7 = ["Masukan dalam urutan bit terbalik", "Tahap 1: butterfly dua titik",
           "Tahap 2: butterfly empat titik", "Tahap 3: hasil DFT delapan titik"]
for index, (a, values, title) in enumerate(zip(ax.flat, stages7, titles7)):
    complex_stem(a, values)
    a.set(title=title, xlabel="Bin k" if index == 3 else "Posisi larik", ylabel="Nilai kompleks")
fig.suptitle("Soal 7: seluruh tahap FFT DIT", fontsize=14, fontweight="bold")
save(fig, 7)

# Soal 8: DIF empat titik dan hitungan operasi kompleks untuk N = 16.
X8, raw8, stages8, permutation8 = fft_dif_stages([1, 2, 3, 4])
np.testing.assert_allclose(stages8[1], [4, 6, -2, 2j], atol=1e-12)
np.testing.assert_allclose(raw8, [10, -2, -2+2j, -2-2j], atol=1e-12)
np.testing.assert_allclose(X8, [10, -2+2j, -2, -2-2j], atol=1e-12)
np.testing.assert_allclose(X8, np.fft.fft([1, 2, 3, 4]), atol=1e-12)
N8 = 16
counts_direct = np.array([N8**2, N8*(N8-1)])
counts_fft = np.array([N8//2 * 4, N8 * 4])
np.testing.assert_array_equal(counts_direct, [256, 240])
np.testing.assert_array_equal(counts_fft, [32, 64])
fig = plt.figure(figsize=(12, 7), constrained_layout=True)
gs = fig.add_gridspec(2, 2)
a = fig.add_subplot(gs[0, 0])
complex_stem(a, raw8)
a.set(title="DIF empat titik: urutan mentah X0, X2, X1, X3", xlabel="Posisi larik", ylabel="Nilai")
a = fig.add_subplot(gs[0, 1])
complex_stem(a, X8)
a.set(title="Setelah penataan: urutan frekuensi biasa", xlabel="Bin k", ylabel="Nilai")
a = fig.add_subplot(gs[1, :])
positions = np.arange(2)
bars1 = a.bar(positions-0.18, counts_direct, 0.36, color=BLUE, label="DFT langsung")
bars2 = a.bar(positions+0.18, counts_fft, 0.36, color=ORANGE, label="FFT radix-2")
for bar in list(bars1)+list(bars2):
    a.text(bar.get_x()+bar.get_width()/2, bar.get_height()+5,
           str(int(bar.get_height())), ha="center")
a.set(title="Soal 8: hitungan operasi dasar pada N = 16",
      xticks=positions, xticklabels=["Perkalian kompleks", "Penjumlahan/pengurangan kompleks"],
      ylabel="Jumlah operasi", ylim=(0, 295))
a.legend(fontsize=9)
save(fig, 8)

# Soal 9: IDFT langsung dan invers melalui dua konjugasi.
X9, Y9 = np.array([4, 0, 0, 0]), np.array([0, 4, 0, 0])
x9, y9 = idft(X9), idft(Y9)
Y9_conj = np.conj(Y9)
B9 = dft(Y9_conj)
y9_via_fft = np.conj(np.fft.fft(Y9_conj))/4
np.testing.assert_allclose(x9, [1, 1, 1, 1], atol=1e-12)
np.testing.assert_allclose(y9, [1, 1j, -1, -1j], atol=1e-12)
np.testing.assert_allclose(B9, [4, -4j, -4, 4j], atol=1e-12)
np.testing.assert_allclose(y9_via_fft, y9, atol=1e-12)
np.testing.assert_allclose(y9, np.fft.ifft(Y9), atol=1e-12)
fig, ax = plt.subplots(2, 2, figsize=(11, 6.4), constrained_layout=True)
for a, values, name in [(ax[0, 0], X9, "Spektrum X: hanya bin DC"),
                         (ax[0, 1], Y9, "Spektrum Y: hanya bin satu")]:
    stem(a, np.arange(4), values, annotate=True)
    a.set(title=name, xlabel="Bin k", ylabel="Nilai spektrum")
complex_stem(ax[1, 0], x9)
ax[1, 0].set(title="Invers X: barisan real konstan", xlabel="Indeks n", ylabel="x[n]")
complex_stem(ax[1, 1], y9)
ax[1, 1].set(title="Invers Y: eksponensial kompleks", xlabel="Indeks n", ylabel="y[n]")
fig.suptitle("Soal 9: invers DFT empat titik", fontweight="bold", fontsize=14)
save(fig, 9)

# Soal 10: melengkapi simetri dan energi blok enam sampel.
X10 = np.array([3, 1-2j, -1+1j, 2, -1-1j, 1+2j])
np.testing.assert_allclose(X10[(-np.arange(6))%6], X10.conj(), atol=1e-12)
energy10 = np.abs(X10)**2 / 6
x10 = idft(X10)
np.testing.assert_allclose(x10.imag, 0, atol=1e-12)
np.testing.assert_allclose(energy10.sum(), 4.5, atol=1e-12)
np.testing.assert_allclose(np.sum(np.abs(x10)**2), 4.5, atol=1e-12)
np.testing.assert_allclose(dft(x10), X10, atol=1e-12)
fig, ax = plt.subplots(3, 1, figsize=(11, 7.5), constrained_layout=True)
stem(ax[0], np.arange(6), X10.real, annotate=True)
ax[0].set(title="Soal 10: bagian real simetris secara siklik", xlabel="Bin k", ylabel="Re X[k]")
stem(ax[1], np.arange(6), X10.imag, ORANGE, annotate=True)
ax[1].set(title="Bagian imajiner berlawanan tanda pada pasangan bin", xlabel="Bin k", ylabel="Im X[k]")
ax[2].bar(np.arange(6), energy10, color=GREEN, alpha=0.85)
ax[2].set(title="Kontribusi energi per bin; jumlah = 4,5", xlabel="Bin k",
          ylabel="|X[k]| kuadrat / 6", xticks=range(6))
save(fig, 10)

print("\nRingkasan pemeriksaan numerik:")
print("Soal 1, DFT:", np.round(X1, 6))
print("Soal 2, DFT:", np.round(X2, 6), "; energi:", energy2.sum())
print("Soal 3, DFT dua titik:", np.round(DFT2, 6), "; empat titik:", np.round(DFT4, 6))
print("Soal 4, Y:", np.round(Y4, 6), "; Z:", np.round(Z4, 6))
print("Soal 5, siklik:", yc5, "; linear:", linear5)
print("Soal 6, P minimum:", P6, "; keluaran:", np.round(yp5, 6))
print("Soal 7, urutan bit terbalik:", permutation7)
for stage, values in enumerate(stages7):
    print(f"  Tahap DIT {stage}:", np.round(values, 6))
print("Soal 8, tahap DIF:")
for stage, values in enumerate(stages8):
    print(f"  Tahap DIF {stage}:", np.round(values, 6))
print("  Urutan biasa:", np.round(X8, 6))
print("  Operasi DFT:", counts_direct, "; FFT:", counts_fft)
print("Soal 9, invers X:", np.round(x9, 6), "; invers Y:", np.round(y9, 6))
print("Soal 10, energi:", energy10.sum(), "; galat imajiner invers:", np.max(np.abs(x10.imag)))
print("Semua pemeriksaan lulus. Sepuluh PNG telah dibuat.")
