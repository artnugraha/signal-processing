"""Hitung ulang dan gambar solusi latihan hitungan tangan Pertemuan 3.

Jalankan: python Kode/solusi-kuliah-03/buat_gambar_solusi_03.py
Dependensi: numpy dan matplotlib. Semua indeks awal dinyatakan eksplisit.
Gambar disimpan relatif terhadap lokasi skrip, bukan direktori terminal.
"""

from pathlib import Path
from io import BytesIO
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Skrip menyimpan PNG tanpa memerlukan desktop.
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Gambar" / "solusi-kuliah-03"
OUT.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN = "#175c9a", "#cf641e", "#188479"
plt.rcParams.update({
    "font.size": 11, "figure.dpi": 110,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.18,
    "axes.titleweight": "bold", "axes.titlesize": 12,
})


def stem(ax, n, y, color=BLUE, label=None, marker="o", annotate=False):
    n, y = np.asarray(n), np.asarray(y)
    ax.vlines(n, 0, y, color=color, lw=1.8, alpha=0.8)
    ax.plot(n, y, linestyle="none", marker=marker, ms=6,
            color=color, label=label)
    ax.axhline(0, color="0.35", lw=0.7)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if annotate:
        for ni, yi in zip(n, y):
            txt = str(int(yi)) if float(yi).is_integer() else f"{yi:.2f}"
            ax.annotate(txt, (ni, yi), xytext=(0, 7 if yi >= 0 else -14),
                        textcoords="offset points", ha="center", fontsize=10)
    ax.margins(x=0.08, y=0.25)


def save(fig, number):
    # BytesIO memastikan PNG ditulis lengkap setelah proses render selesai.
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=170, bbox_inches="tight", facecolor="white")
    path = OUT / f"soal-{number:02d}.png"
    path.write_bytes(buf.getvalue())
    plt.close(fig)
    print(f"Gambar {number:02d}: {path.name}")


def zero_sample(values, indices, start=0):
    """Baca barisan berhingga dengan perpanjangan nol dan indeks awal tertentu."""
    values = np.asarray(values)
    indices = np.asarray(indices)
    local = indices - start
    out = np.zeros(indices.shape, dtype=float)
    inside = (local >= 0) & (local < len(values))
    out[inside] = values[local[inside]]
    return out


def cross_correlation(a, b):
    """r_ab(j) = sum_n a[n] b[n+j] / N, dengan pembagi tetap."""
    a, b = np.asarray(a), np.asarray(b)
    assert len(a) == len(b)
    N = len(a)
    lags = np.arange(-N + 1, N)
    values = np.array([
        sum(a[n] * b[n+j] for n in range(N) if 0 <= n+j < N) / N
        for j in lags
    ])
    # Urutan argumen NumPy disesuaikan dengan definisi di atas.
    np.testing.assert_allclose(values, np.correlate(b, a, mode="full") / N)
    return lags, values


# Soal 1. x dimulai pada n = -1; h dimulai pada n = 0.
h = np.array([1, 2, -1])
n = np.arange(-1, 5)
c1 = 2 * zero_sample(h, n + 1)
c2 = -zero_sample(h, n)
c3 = 3 * zero_sample(h, n - 2)
y1 = c1 + c2 + c3
np.testing.assert_array_equal(y1, [2, 3, -4, 4, 6, -3])
np.testing.assert_array_equal(y1, np.convolve([2, -1, 0, 3], h))
fig, ax = plt.subplots(2, 1, figsize=(10, 6.2), sharex=True, constrained_layout=True)
for values, color, label, marker in [
    (c1, BLUE, r"$2h[n+1]$", "o"), (c2, ORANGE, r"$-h[n]$", "s"),
    (c3, GREEN, r"$3h[n-2]$", "^")]:
    stem(ax[0], n, values, color, label, marker)
ax[0].set(title="Soal 1: kontribusi respons impuls tergeser", ylabel="Amplitudo")
ax[0].legend(ncol=3, loc="upper left", fontsize=10)
stem(ax[1], n, y1, annotate=True)
ax[1].set(title="Jumlah ketiga kontribusi", xlabel="Indeks n", ylabel="y[n]")
for a in ax:
    a.axvline(0, color="0.5", ls="--", lw=0.8)
save(fig, 1)

# Soal 2. Konvolusi langsung.
x2, h2 = np.array([1, -2, 3, 1]), np.array([2, 0, -1])
y2 = np.convolve(x2, h2)
np.testing.assert_array_equal(y2, [2, -4, 5, 4, -3, -1])
fig, ax = plt.subplots(3, 1, figsize=(10, 7), constrained_layout=True)
for a, values, name in zip(ax, [x2, h2, y2], ["x[n]", "h[n]", "y[n] = x[n] * h[n]"]):
    stem(a, np.arange(len(values)), values, annotate=True)
    a.set(xlim=(-0.5, 5.5), ylabel=name)
ax[0].set_title("Soal 2: konvolusi linear dua barisan berhingga")
ax[-1].set_xlabel("Indeks n")
save(fig, 2)

# Soal 3. Tumpang tindih pada konvolusi diskret.
y3 = np.convolve(np.ones(4, dtype=int), np.ones(3, dtype=int))
np.testing.assert_array_equal(y3, [1, 2, 3, 3, 2, 1])
fig = plt.figure(figsize=(11, 8), constrained_layout=True)
gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1.1])
k = np.arange(-3, 7)
for i, shift in enumerate([0, 2, 3, 4]):
    a = fig.add_subplot(gs[i // 2, i % 2])
    xv = ((k >= 0) & (k <= 3)).astype(int)
    hv = ((k >= shift - 2) & (k <= shift)).astype(int)
    stem(a, k, xv, BLUE, "x[k]", "o")
    a.scatter(k, hv, marker="s", s=60, facecolors="none", edgecolors=ORANGE,
              linewidths=1.5, label="h[n-k]", zorder=4)
    overlap = k[(xv * hv) == 1]
    a.scatter(overlap, np.ones(len(overlap)), s=150, facecolors="none",
              edgecolors=GREEN, linewidths=2.0, zorder=5)
    a.set(title=f"n = {shift}: {len(overlap)} pasangan, y[{shift}] = {len(overlap)}",
          xlabel="Indeks penjumlahan k", ylim=(-0.15, 1.65), yticks=[0, 1])
    if i == 0:
        a.legend(loc="upper left", fontsize=9, ncol=2)
a = fig.add_subplot(gs[2, :])
stem(a, np.arange(6), y3, annotate=True)
a.set(title="Soal 3: jumlah produk pada setiap indeks keluaran",
      xlabel="Indeks keluaran n", ylabel="y[n]")
save(fig, 3)

# Soal 4. Dua pengelompokan konvolusi.
h1, h2, h3 = np.array([1, 1]), np.array([1, -1]), np.array([1, 2])
a, b = np.convolve(h1, h2), np.convolve(h2, h3)
yA, yB = np.convolve(a, h3), np.convolve(h1, b)
np.testing.assert_array_equal(yA, [1, 2, -1, -2])
np.testing.assert_array_equal(yA, yB)
fig, ax = plt.subplots(3, 1, figsize=(10, 7), constrained_layout=True)
stem(ax[0], np.arange(len(a)), a, annotate=True)
ax[0].set(title="Soal 4: hasil perantara a[n] = h1 * h2", ylabel="a[n]")
stem(ax[1], np.arange(len(b)), b, ORANGE, annotate=True)
ax[1].set(title="Hasil perantara b[n] = h2 * h3", ylabel="b[n]")
stem(ax[2], np.arange(4), yA, BLUE, "(h1 * h2) * h3", annotate=True)
ax[2].scatter(np.arange(4), yB, s=110, facecolors="none", edgecolors=ORANGE,
              marker="s", label="h1 * (h2 * h3)", zorder=4)
ax[2].set(title="Kedua hasil akhir berimpit", xlabel="Indeks n", ylabel="Keluaran")
ax[2].legend(loc="upper right", fontsize=9)
save(fig, 4)

# Soal 5. Konvolusi siklik dan matriks sirkulan.
x5, h5 = np.array([2, 1, 0, 3]), np.array([1, -1, 2, 0])
H = np.array([[h5[(n-k) % 4] for k in range(4)] for n in range(4)])
yc = H @ x5
manual_cyclic = np.array([sum(x5[k] * h5[(n-k) % 4] for k in range(4)) for n in range(4)])
np.testing.assert_array_equal(yc, [-1, 5, 3, 5])
np.testing.assert_array_equal(yc, manual_cyclic)
linear = np.convolve(x5, h5)
folded = np.zeros(4, dtype=int)
for n, value in enumerate(linear):
    folded[n % 4] += value
np.testing.assert_array_equal(yc, folded)
fig, ax = plt.subplots(1, 2, figsize=(10.5, 4.3), constrained_layout=True)
ax[0].imshow(H, cmap="RdBu", vmin=-2, vmax=2)
for row in range(4):
    for col in range(4):
        ax[0].text(col, row, str(H[row, col]), ha="center", va="center",
                   fontsize=16, color="white" if abs(H[row, col]) == 2 else "black")
ax[0].set(title="Matriks H: h[(n-k) mod 4]", xlabel="Kolom k", ylabel="Baris n",
          xticks=range(4), yticks=range(4))
ax[0].grid(False)
stem(ax[1], np.arange(4), yc, annotate=True)
ax[1].set(title="Soal 5: satu periode keluaran siklik", xlabel="Indeks n", ylabel="yc[n]")
save(fig, 5)

# Soal 6. Korelasi dan normalisasi energi.
x1, x2 = np.array([1, 2, -1, 2]), np.array([2, 4, -2, 4])
r0 = np.dot(x1, x2) / len(x1)
rho = r0 / (np.sqrt(np.dot(x1, x1) * np.dot(x2, x2)) / len(x1))
assert r0 == 5 and rho == 1
fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True, constrained_layout=True)
stem(ax[0], np.arange(4), x1, BLUE, "x1[n]")
stem(ax[0], np.arange(4), x2, ORANGE, "x2[n] = 2 x1[n]", "s")
ax[0].set(title="Soal 6: bentuk sama, amplitudo berbeda", ylabel="Amplitudo")
ax[0].legend(loc="upper left", fontsize=9)
stem(ax[1], np.arange(4), x1, BLUE, "x1[n]")
ax[1].scatter(np.arange(4), x2 / 2, s=100, facecolors="none", edgecolors=ORANGE,
              marker="s", label="x2[n] / 2", zorder=4)
ax[1].set(title="Setelah skala amplitudo disamakan: rho(0) = 1", xlabel="Indeks n", ylabel="Amplitudo")
ax[1].legend(loc="upper left", fontsize=9)
save(fig, 6)

# Soal 7. Korelasi silang dengan konvensi lag sesuai catatan.
x1, x2 = np.array([1, 0, 2, 0, 1]), np.array([0, 1, 0, 2, 0])
lag7, r7 = cross_correlation(x1, x2)
np.testing.assert_allclose(r7, np.array([0, 1, 0, 4, 0, 5, 0, 2, 0]) / 5)
assert lag7[np.argmax(r7)] == 1
fig, ax = plt.subplots(3, 1, figsize=(10, 7.3), constrained_layout=True)
stem(ax[0], np.arange(5), x1, annotate=True)
ax[0].set(title="Soal 7: barisan referensi", ylabel="x1[n]", xlabel="Indeks n")
stem(ax[1], np.arange(5), x2, ORANGE, annotate=True)
ax[1].set(title="Barisan kedua: pola terlambat satu sampel", ylabel="x2[n]", xlabel="Indeks n")
stem(ax[2], lag7, r7, annotate=True)
ax[2].axvline(0, color="0.4", lw=0.8, ls="--")
ax[2].scatter([1], [1], s=140, edgecolors=GREEN, facecolors="none", lw=2, zorder=4)
ax[2].set(title="Korelasi dengan pembagi tetap N = 5; puncak pada j = +1",
          xlabel="Lag j", ylabel="r12(j)")
save(fig, 7)

# Soal 8. Autokorelasi lengkap.
x8 = np.array([1, -1, 2])
lag8, r8 = cross_correlation(x8, x8)
np.testing.assert_allclose(r8, np.array([2, -3, 6, -3, 2]) / 3)
np.testing.assert_allclose(r8, r8[::-1])
assert lag8[np.argmax(r8)] == 0
fig, ax = plt.subplots(2, 1, figsize=(10, 6), constrained_layout=True)
stem(ax[0], np.arange(3), x8, annotate=True)
ax[0].set(title="Soal 8: barisan masukan", xlabel="Indeks n", ylabel="x[n]")
stem(ax[1], lag8, r8)
for j, value, label in zip(lag8, r8, ["2/3", "-1", "2", "-1", "2/3"]):
    ax[1].annotate(label, (j, value), xytext=(0, 8 if value >= 0 else -15),
                   textcoords="offset points", ha="center")
ax[1].axvline(0, color="0.4", ls="--", lw=0.8)
ax[1].set(title="Autokorelasi genap; maksimum pada lag nol",
          xlabel="Lag j", ylabel="rxx(j)")
save(fig, 8)

# Soal 9. Gabungan seri-paralel dan keluaran sistem.
g = np.array([1, -1]) + np.array([2, 0])
q = np.convolve([1, 1], g)
htotal = q + np.array([1, 0, 0])
y9 = np.convolve([1, 2], htotal)
np.testing.assert_array_equal(htotal, [4, 2, -1])
np.testing.assert_array_equal(y9, [4, 10, 3, -2])
np.testing.assert_array_equal(y9, np.array([1, 2, 0, 0]) + np.convolve([1, 2], q))
fig, ax = plt.subplots(2, 2, figsize=(11, 6), constrained_layout=True)
for a, values, title in zip(ax.flat, [g, q, htotal, y9],
                           ["g = h3 + h4", "q = h2 * g", "h = h1 + q", "y = x * h"]):
    stem(a, np.arange(len(values)), values, annotate=True)
    a.set(title=title, xlabel="Indeks n", ylabel="Amplitudo")
fig.suptitle("Soal 9: penyederhanaan sistem seri–paralel", fontsize=14, fontweight="bold")
save(fig, 9)

# Soal 10. Konvolusi kontinu sebagai panjang perpotongan interval.
def y_continuous(t):
    t = np.asarray(t)
    return np.maximum(0, np.minimum(2, t) - np.maximum(0, t - 3))

# Verifikasi integral dengan jumlah Riemann bertitik tengah.
dtau = 0.0005
tau = np.arange(-4, 7, dtau) + dtau / 2
xp = ((tau >= 0) & (tau < 2)).astype(float)
check_times = np.array([-1, 0, 0.7, 2, 2.5, 3, 4.2, 5, 6])
integrals = np.array([
    np.sum(xp * ((time-tau >= 0) & (time-tau < 3))) * dtau
    for time in check_times
])
np.testing.assert_allclose(integrals, y_continuous(check_times), atol=2 * dtau, rtol=0)

fig = plt.figure(figsize=(11, 8), constrained_layout=True)
gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1.2])
for i, time in enumerate([0.8, 2.5, 4.0, 5.5]):
    a = fig.add_subplot(gs[i // 2, i % 2])
    a.plot([-4, 0, 0, 2, 2, 7], [0, 0, 1, 1, 0, 0], color=BLUE, lw=2, label="x(tau)")
    a.plot([-4, time-3, time-3, time, time, 7], [0, 0, 1, 1, 0, 0],
           color=ORANGE, lw=2, ls="--", label="h(t-tau)")
    left, right = max(0, time-3), min(2, time)
    if right > left:
        a.fill_between([left, right], 0, 1, color=GREEN, alpha=0.25)
    a.set(xlim=(-3.5, 6), ylim=(-0.08, 1.55), yticks=[0, 1], xlabel=r"$\tau$",
          title=f"t = {time:g}: luas tumpang tindih = {float(y_continuous(time)):g}")
    if i == 0:
        a.legend(loc="upper right", fontsize=9)
a = fig.add_subplot(gs[2, :])
tt = np.linspace(-1, 6, 1401)
a.plot(tt, y_continuous(tt), color=BLUE, lw=2.5)
a.fill_between(tt, y_continuous(tt), color=BLUE, alpha=0.08)
for time, value in [(0, 0), (2, 2), (3, 2), (5, 0)]:
    a.plot(time, value, "o", color=ORANGE)
    a.annotate(f"({time}, {value})", (time, value), xytext=(0, 10),
               textcoords="offset points", ha="center", fontsize=10)
a.set(xlim=(-1, 6), ylim=(-0.15, 2.65), title="Soal 10: konvolusi kontinu berbentuk trapesium",
      xlabel="Waktu t", ylabel="y(t)", xticks=[0, 1, 2, 3, 4, 5])
save(fig, 10)

print("\nHasil pemeriksaan numerik:")
print("Soal 1, n=-1..4 :", y1.astype(int))
print("Soal 2, n=0..5  :", y2)
print("Soal 3, n=0..5  :", y3)
print("Soal 4, n=0..3  :", yA)
print("Soal 5, n=0..3  :", yc)
print("Soal 6           : r12(0)=", r0, "; rho12(0)=", rho)
print("Soal 7, j=-4..4 :", r7)
print("Soal 8, j=-2..2 :", r8)
print("Soal 9           : h=", htotal, "; y=", y9)
print("Soal 10: galat maksimum integral numerik =",
      np.max(np.abs(integrals - y_continuous(check_times))))
print("Semua pemeriksaan lulus. Sepuluh PNG telah dibuat.")
