"""Gambar dan pemeriksaan numerik solusi latihan hitungan Pertemuan 4.

Jalankan dari folder mana pun:
    python Kode/solusi-kuliah-04/buat_gambar_solusi_04.py
Dependensi: numpy, matplotlib. Tidak memakai FFT atau SciPy.
Lokasi keluaran ditentukan relatif terhadap lokasi skrip.
"""
from pathlib import Path
from io import BytesIO
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Gambar" / "solusi-kuliah-04"
OUT.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN = "#175c9a", "#ce641d", "#188479"
plt.rcParams.update({
    "font.size": 11, "figure.dpi": 110,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.18,
    "axes.titleweight": "bold", "axes.titlesize": 12,
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
            label_value = 0.0 if abs(yi) < 1e-12 else yi
            ax.annotate(f"{label_value:g}", (ni, yi), xytext=(0, 8 if yi >= 0 else -15),
                        textcoords="offset points", ha="center", fontsize=10)
    ax.margins(x=0.08, y=0.25)


def dtft(samples, n, Omega):
    """DTFT langsung pada kisi Omega, dengan indeks waktu n eksplisit."""
    return np.exp(-1j * np.outer(Omega, n)) @ np.asarray(samples)


def phase_for_plot(z, zero_tol=1e-10):
    """Fase utama dengan titik nol dan garis penghubung lompatan dihilangkan."""
    z = np.asarray(z)
    phase = (np.angle(z) + np.pi) % (2*np.pi) - np.pi
    phase[np.abs(z) < zero_tol] = np.nan
    jumps = np.flatnonzero(np.abs(np.diff(phase)) > np.pi) + 1
    phase[jumps] = np.nan
    return phase


def midpoint_ft(function, left, right, count, frequencies):
    """Pendekatan integral Fourier dengan aturan titik tengah."""
    dt = (right - left) / count
    t = left + (np.arange(count) + 0.5) * dt
    values = function(t)
    return np.array([np.sum(values * np.exp(-1j * w * t)) * dt
                     for w in frequencies])


# Soal 1: dua frekuensi analog dengan sampel kosinus identik.
fs = 800
n1 = np.arange(17)
ts = n1 / fs
samples100 = 4 * np.cos(2 * np.pi * 100 * ts + np.pi / 4)
samples900 = 4 * np.cos(2 * np.pi * 900 * ts + np.pi / 4)
euler = (2 * np.exp(1j * np.pi / 4) * np.exp(1j * 200 * np.pi * ts)
         + 2 * np.exp(-1j * np.pi / 4) * np.exp(-1j * 200 * np.pi * ts))
np.testing.assert_allclose(samples100, samples900, atol=1e-11)
np.testing.assert_allclose(euler, samples100, atol=1e-12)
fig, ax = plt.subplots(2, 1, figsize=(11, 6.5), constrained_layout=True)
tt = np.linspace(0, 0.02, 6001)
ax[0].plot(1000*tt, 4*np.cos(2*np.pi*900*tt + np.pi/4), color=ORANGE,
           lw=1, alpha=0.7, label="900 Hz")
ax[0].plot(1000*tt, 4*np.cos(2*np.pi*100*tt + np.pi/4), color=BLUE,
           lw=2, label="100 Hz")
ax[0].plot(1000*ts, samples100, "ko", ms=4, label="Sampel pada 800 Hz")
ax[0].set(title="Soal 1: dua sinyal kontinu berbeda, sampel sama",
          xlabel="Waktu t (ms)", ylabel="Amplitudo", xlim=(0, 20))
ax[0].legend(fontsize=9, loc="upper right", ncol=3)
stem(ax[1], n1, samples100, BLUE, "Sampel 100 Hz")
ax[1].scatter(n1, samples900, s=70, facecolors="none", edgecolors=ORANGE,
              marker="s", label="Sampel 900 Hz", zorder=4)
ax[1].set(xlabel="Indeks sampel n", ylabel="x[n]", title="Kedua barisan berimpit")
ax[1].legend(loc="upper right", fontsize=9)
save(fig, 1)

# Soal 2: koefisien FS, sintesis, dan daya Parseval.
harmonics = np.array([-2, -1, 0, 1, 2])
C = np.array([-1j, 1.5, 2, 1.5, 1j])
theta = np.linspace(0, 2*np.pi, 6000, endpoint=False)
x_real = 2 + 3*np.cos(theta) - 2*np.sin(2*theta)
x_fs = np.exp(1j * np.outer(theta, harmonics)) @ C
np.testing.assert_allclose(x_fs, x_real, atol=1e-12)
C_numerical = np.mean(x_real[:, None] * np.exp(-1j*np.outer(theta, harmonics)), axis=0)
np.testing.assert_allclose(C_numerical, C, atol=1e-12)
power_fs = np.sum(np.abs(C)**2)
power_time = np.mean(x_real**2)
np.testing.assert_allclose(power_fs, 10.5, atol=1e-12)
np.testing.assert_allclose(power_fs, power_time, atol=1e-12)
fig = plt.figure(figsize=(11, 7), constrained_layout=True)
gs = fig.add_gridspec(2, 2)
a = fig.add_subplot(gs[0, :])
a.plot(theta / np.pi, x_real, color=BLUE, lw=2, label="Bentuk real")
a.plot(theta[::120] / np.pi, x_fs.real[::120], "o", color=ORANGE, ms=3,
        label="Sintesis eksponensial")
a.set(title="Soal 2: sintesis FS; daya rata-rata = 10,5",
      xlabel=r"$\omega_0 t/\pi$", ylabel="x(t)")
a.legend(fontsize=9)
a = fig.add_subplot(gs[1, 0])
stem(a, harmonics, np.abs(C), annotate=True)
a.set(title="Magnitudo koefisien dua sisi", xlabel="Harmonik k", ylabel=r"$|C_k|$")
a = fig.add_subplot(gs[1, 1])
stem(a, harmonics, np.angle(C) / np.pi)
a.set(title="Fase koefisien tak nol", xlabel="Harmonik k", ylabel=r"$\angle C_k /\pi$",
      yticks=[-0.5, 0, 0.5])
save(fig, 2)

# Soal 3: pulsa periodik tinggi 2, lebar 1, periode 4.
def pulse_coeff(k):
    return 0.5 * np.sinc(np.asarray(k) / 4)

selected_C = pulse_coeff(np.array([0, 1, 2, 4]))
np.testing.assert_allclose(selected_C, [0.5, np.sqrt(2)/np.pi, 1/np.pi, 0], atol=1e-14)
k3 = np.arange(-16, 17)
mid = -0.5 + (np.arange(20000) + 0.5) / 20000
C_mid = np.array([0.5 * np.mean(np.exp(-1j*k*np.pi*mid/2)) for k in k3])
np.testing.assert_allclose(C_mid, pulse_coeff(k3), atol=1e-8)
tp = np.linspace(-2, 2, 4001)
fig, ax = plt.subplots(2, 1, figsize=(11, 7), constrained_layout=True)
ax[0].plot([-2, -0.5, -0.5, 0.5, 0.5, 2], [0, 0, 2, 2, 0, 0],
           color="0.35", lw=1.6, label="Pulsa ideal")
for K, color in [(5, ORANGE), (40, BLUE)]:
    k = np.arange(-K, K+1)
    reconstruction = np.exp(1j*np.outer(tp, k*np.pi/2)) @ pulse_coeff(k)
    ax[0].plot(tp, reconstruction.real, color=color, lw=1.2, label=f"FS: K = {K}")
ax[0].scatter([-0.5, 0.5], [1, 1], color=GREEN, zorder=5,
              label="Limit FS pada lompatan = 1")
ax[0].set(title="Soal 3: rekonstruksi satu periode pulsa", xlabel="Waktu t (s)",
          ylabel="Amplitudo", xlim=(-2, 2), ylim=(-0.35, 2.45))
ax[0].legend(loc="upper right", fontsize=9)
stem(ax[1], k3, pulse_coeff(k3))
ax[1].set(title="Koefisien FS real: tanda koefisien tetap ditampilkan",
          xlabel="Harmonik k", ylabel="Ck")
save(fig, 3)

# Soal 4: FT pulsa tinggi 3 pada 1 < t < 3.
w4 = np.linspace(-4*np.pi, 4*np.pi, 4001)
X4 = 6 * np.sinc(w4 / np.pi) * np.exp(-2j*w4)
wcheck4 = np.array([-7, -np.pi, -1, 0, 1, np.pi, 7])
integral4 = midpoint_ft(lambda t: np.full_like(t, 3.0), 1, 3, 40000, wcheck4)
theory4 = 6 * np.sinc(wcheck4/np.pi) * np.exp(-2j*wcheck4)
np.testing.assert_allclose(integral4, theory4, atol=1e-8)
fig, ax = plt.subplots(3, 1, figsize=(11, 8), constrained_layout=True)
ax[0].plot([-1, 1, 1, 3, 3, 5], [0, 0, 3, 3, 0, 0], color=BLUE, lw=2)
ax[0].axvline(2, color=ORANGE, ls="--", lw=1, label="Pusat pada t = 2 s")
ax[0].set(title="Soal 4: pulsa berpusat di nol yang ditunda 2 s",
          xlabel="Waktu t (s)", ylabel="x(t)", ylim=(-0.2, 3.7))
ax[0].legend(fontsize=9)
ax[1].plot(w4 / np.pi, np.abs(X4), color=BLUE, lw=1.8)
ax[1].plot([-1, 1], [0, 0], "o", color=ORANGE, label="Nol pertama")
ax[1].set(xlabel=r"$\omega/\pi$ (rad/s dibagi pi)", ylabel=r"$|X(\omega)|$",
          title="Magnitudo tidak berubah oleh penundaan")
ax[1].legend(fontsize=9)
wm = np.linspace(-np.pi, np.pi, 1601)
Xm = 6 * np.sinc(wm / np.pi) * np.exp(-2j*wm)
continuous_phase = -2*wm
continuous_phase[[0, -1]] = np.nan
ax[2].plot(wm / np.pi, continuous_phase / np.pi, color=ORANGE, ls="--",
           lw=1.8, label="Cabang kontinu: -2 omega")
ax[2].plot(wm / np.pi, phase_for_plot(Xm) / np.pi, color=BLUE, lw=1.5,
           label="Fase utama")
ax[2].set(title="Fase pada lobus utama; fase di nol spektrum dihilangkan",
          xlabel=r"$\omega/\pi$", ylabel="Fase / pi", xlim=(-1, 1))
ax[2].legend(fontsize=9, loc="upper right")
save(fig, 4)

# Soal 5: integral FT eksponensial dan simetri konjugat.
w5 = np.linspace(-15, 15, 3001)
X5 = 2 / (3 + 1j*w5)
np.testing.assert_allclose(X5[::-1], np.conj(X5), atol=1e-12)
wcheck5 = np.array([-8, -3, 0, 3, 8])
integral5 = midpoint_ft(lambda t: 2*np.exp(-3*t), 0, 8, 80000, wcheck5)
np.testing.assert_allclose(integral5, 2/(3+1j*wcheck5), atol=1e-8)
np.testing.assert_allclose(2/(3+3j), (1-1j)/3, atol=1e-14)
fig, ax = plt.subplots(3, 1, figsize=(11, 7.5), constrained_layout=True)
time5 = np.linspace(-0.5, 2, 1501)
signal5 = np.where(time5 >= 0, 2*np.exp(-3*time5), 0)
ax[0].plot(time5, signal5, color=BLUE)
ax[0].set(title="Soal 5: eksponensial kausal", xlabel="Waktu t (s)", ylabel="x(t)")
ax[1].plot(w5, np.abs(X5), color=BLUE)
ax[1].scatter([-3, 0, 3], [np.sqrt(2)/3, 2/3, np.sqrt(2)/3], color=ORANGE)
ax[1].set(title="Magnitudo genap", xlabel="omega (rad/s)", ylabel=r"$|X(\omega)|$")
ax[2].plot(w5, np.angle(X5)/np.pi, color=BLUE)
ax[2].scatter([-3, 0, 3], [0.25, 0, -0.25], color=ORANGE)
ax[2].set(title="Fase ganjil", xlabel="omega (rad/s)", ylabel="Fase / pi")
save(fig, 5)

# Soal 6: DTFT tiga sampel dan fase pada nol spektrum.
Omega = np.linspace(-np.pi, np.pi, 2401)
X6_direct = dtft([1, 2, 1], np.arange(3), Omega)
X6 = 4*np.exp(-1j*Omega)*np.cos(Omega/2)**2
np.testing.assert_allclose(X6_direct, X6, atol=1e-12)
np.testing.assert_allclose(dtft([1, 2, 1], np.arange(3), [0, np.pi/2, np.pi]),
                           [4, -2j, 0], atol=1e-12)
fig, ax = plt.subplots(3, 1, figsize=(11, 7.5), constrained_layout=True)
stem(ax[0], np.arange(3), [1, 2, 1], annotate=True)
ax[0].set(title="Soal 6: tiga sampel berhingga", xlabel="Indeks n", ylabel="x[n]")
ax[1].plot(Omega/np.pi, np.abs(X6), color=BLUE, lw=2)
ax[1].scatter([0, 0.5, 1], [4, 2, 0], color=ORANGE, zorder=3)
ax[1].set(title="Magnitudo DTFT", xlabel=r"$\Omega/\pi$", ylabel=r"$|X(e^{j\Omega})|$")
ax[2].plot(Omega/np.pi, phase_for_plot(X6)/np.pi, color=BLUE, lw=2)
ax[2].plot([-1, 1], [1, -1], "o", mfc="none", mec=ORANGE, ms=7)
ax[2].set(title="Fase pada -pi < Omega < pi; ujung terbuka = fase tidak terdefinisi",
          xlabel=r"$\Omega/\pi$", ylabel="Fase / pi", xlim=(-1.06, 1.06))
save(fig, 6)

# Soal 7: DTFT deret geometri dan kesamaan nilai kompleks pada dua frekuensi.
O7 = np.linspace(-np.pi, 3*np.pi, 3601)
X7 = 1/(1-0.5*np.exp(-1j*O7))
X7_sum = dtft(0.5**np.arange(80), np.arange(80), O7)
np.testing.assert_allclose(X7_sum, X7, atol=1e-12)
test_O7 = np.array([0, np.pi, np.pi/3, 7*np.pi/3])
test_X7 = 1/(1-0.5*np.exp(-1j*test_O7))
np.testing.assert_allclose(test_X7, [2, 2/3, 1-1j/np.sqrt(3), 1-1j/np.sqrt(3)], atol=1e-12)
fig, ax = plt.subplots(2, 1, figsize=(11, 6), sharex=True, constrained_layout=True)
for a, values, selected, label in [
    (ax[0], X7.real, test_X7[2:].real, "Bagian real"),
    (ax[1], X7.imag, test_X7[2:].imag, "Bagian imajiner")]:
    a.plot(O7/np.pi, values, color=BLUE, lw=1.8)
    a.scatter(test_O7[2:]/np.pi, selected, color=ORANGE, zorder=3)
    for pos in [1/3, 7/3]:
        a.axvline(pos, color=ORANGE, ls="--", lw=0.8, alpha=0.5)
    a.axvspan(0, 2, color=GREEN, alpha=0.05)
    a.set(ylabel=label, xlim=(-1, 3), xticks=[-1, 0, 1/3, 1, 2, 7/3, 3],
          xticklabels=["-1", "0", "1/3", "1", "2", "7/3", "3"])
ax[0].set_title("Soal 7: nilai kompleks berulang setelah pergeseran 2 pi")
ax[1].set_xlabel(r"$\Omega/\pi$")
save(fig, 7)

# Soal 8: urutan penundaan kemudian modulasi.
n8 = np.array([2, 3])
y8 = np.array([-1, -1j])
Y8_direct = dtft(y8, n8, Omega)
Y8_property = np.exp(-2j*(Omega-np.pi/2)) * (1+np.exp(-1j*(Omega-np.pi/2)))
Y8_expanded = -np.exp(-2j*Omega) - 1j*np.exp(-3j*Omega)
np.testing.assert_allclose(Y8_direct, Y8_property, atol=1e-12)
np.testing.assert_allclose(Y8_direct, Y8_expanded, atol=1e-12)
np.testing.assert_allclose(np.exp(1j*np.pi*n8/2), y8, atol=1e-12)
fig, ax = plt.subplots(2, 2, figsize=(11, 6.5), constrained_layout=True)
plot_n8 = np.arange(0, 6)
plot_y8 = np.zeros(6, dtype=complex)
plot_y8[n8] = y8
stem(ax[0, 0], plot_n8, plot_y8.real, annotate=True)
ax[0, 0].set(title="Soal 8: bagian real y[n]", xlabel="Indeks n", ylabel="Re y[n]")
stem(ax[0, 1], plot_n8, plot_y8.imag, ORANGE, annotate=True)
ax[0, 1].set(title="Bagian imajiner y[n]", xlabel="Indeks n", ylabel="Im y[n]")
ax[1, 0].plot(Omega/np.pi, np.abs(Y8_property), color=BLUE, lw=2, label="Sifat transformasi")
ax[1, 0].plot(Omega[::100]/np.pi, np.abs(Y8_direct[::100]), "o",
              color=ORANGE, ms=3, label="DTFT langsung")
ax[1, 0].set(title="Puncak magnitudo bergeser ke pi/2", xlabel=r"$\Omega/\pi$", ylabel="Magnitudo")
ax[1, 0].legend(fontsize=9)
ax[1, 1].plot(Omega/np.pi, phase_for_plot(Y8_direct)/np.pi, color=BLUE)
ax[1, 1].set(title="Fase utama; titik nol spektrum dihilangkan",
              xlabel=r"$\Omega/\pi$", ylabel="Fase / pi")
save(fig, 8)

# Soal 9: perkalian DTFT sama dengan DTFT konvolusi linear.
x9, h9 = np.array([1, -1]), np.array([1, 2, 1])
y9 = np.convolve(x9, h9)
np.testing.assert_array_equal(y9, [1, 1, -1, -1])
X9 = dtft(x9, np.arange(len(x9)), Omega)
H9 = dtft(h9, np.arange(len(h9)), Omega)
Y9 = dtft(y9, np.arange(len(y9)), Omega)
np.testing.assert_allclose(Y9, X9*H9, atol=1e-12)
fig, ax = plt.subplots(2, 2, figsize=(11, 6.5), constrained_layout=True)
for a, values, name in [(ax[0, 0], x9, "x[n]"), (ax[0, 1], h9, "h[n]"),
                         (ax[1, 0], y9, "y[n] = x[n] * h[n]")]:
    stem(a, np.arange(len(values)), values, annotate=True)
    a.set(title=name, xlabel="Indeks n", ylabel="Amplitudo")
ax[1, 1].plot(Omega/np.pi, np.abs(X9*H9), color=BLUE, lw=2, label="Magnitudo XH")
ax[1, 1].plot(Omega[::100]/np.pi, np.abs(Y9[::100]), "o", color=ORANGE,
              ms=3, label="Magnitudo DTFT y")
ax[1, 1].set(title="Kesamaan dalam domain frekuensi", xlabel=r"$\Omega/\pi$", ylabel="Magnitudo")
ax[1, 1].legend(fontsize=9)
fig.suptitle("Soal 9: konvolusi dan perkalian spektrum", fontweight="bold", fontsize=14)
save(fig, 9)

# Soal 10: respons frekuensi, keadaan tunak, dan transien awal nol.
H10 = 1/(1-0.5*np.exp(-1j*Omega))
H0 = 1/(1-0.5*np.exp(-1j*np.pi/2))
np.testing.assert_allclose(H0, 4/5-2j/5, atol=1e-14)
np.testing.assert_allclose(dtft(0.5**np.arange(80), np.arange(80), Omega), H10, atol=1e-12)
n10 = np.arange(30)
x10 = 2*np.cos(np.pi*n10/2)
y10 = np.zeros(len(n10))
previous = 0.0
for k in range(len(n10)):
    y10[k] = 0.5*previous + x10[k]
    previous = y10[k]
yss10 = (8/5)*np.cos(np.pi*n10/2) + (4/5)*np.sin(np.pi*n10/2)
yss_polar = 4/np.sqrt(5)*np.cos(np.pi*n10/2-np.arctan(0.5))
transient10 = (2/5)*0.5**n10
np.testing.assert_allclose(yss10, yss_polar, atol=1e-12)
np.testing.assert_allclose(y10, yss10+transient10, atol=1e-12)
np.testing.assert_allclose((y10-yss10)[1:], 0.5*(y10-yss10)[:-1], atol=1e-12)
np.testing.assert_allclose(y10[:6], [2, 1, -1.5, -0.75, 1.625, 0.8125], atol=1e-12)
fig, ax = plt.subplots(2, 2, figsize=(12, 7), constrained_layout=True)
ax[0, 0].plot(Omega/np.pi, np.abs(H10), color=BLUE)
ax[0, 0].scatter([0.5], [abs(H0)], color=ORANGE)
ax[0, 0].set(title="Soal 10: magnitudo respons frekuensi", xlabel=r"$\Omega/\pi$", ylabel="Penguatan")
ax[0, 1].plot(Omega/np.pi, np.angle(H10)/np.pi, color=BLUE)
ax[0, 1].scatter([0.5], [np.angle(H0)/np.pi], color=ORANGE)
ax[0, 1].set(title="Fase respons frekuensi", xlabel=r"$\Omega/\pi$", ylabel="Fase / pi")
show = n10 <= 16
stem(ax[1, 0], n10[show], y10[show], BLUE, "Keluaran awal nol")
ax[1, 0].plot(n10[show], yss10[show], "s", mfc="none", mec=ORANGE,
              ms=7, label="Keadaan tunak")
ax[1, 0].set(title="Respons awal mendekati keadaan tunak", xlabel="Indeks n", ylabel="Keluaran")
ax[1, 0].legend(fontsize=9, loc="upper right")
show_d = n10 <= 20
ax[1, 1].semilogy(n10[show_d], transient10[show_d], color=BLUE, lw=2,
                  label="(2/5) (1/2)^n")
ax[1, 1].semilogy(n10[show_d], (y10-yss10)[show_d], "o", color=ORANGE,
                  ms=4, label="Selisih hasil rekursi dan keadaan tunak")
ax[1, 1].set(title="Transien meluruh setengah setiap sampel", xlabel="Indeks n", ylabel="d[n] (log)")
ax[1, 1].xaxis.set_major_locator(MaxNLocator(integer=True))
ax[1, 1].legend(fontsize=8, loc="upper right")
save(fig, 10)

print("\nRingkasan pemeriksaan:")
print("Soal 1: galat maksimum sampel 100 vs 900 Hz =", np.max(np.abs(samples100-samples900)))
print("Soal 2: daya FS =", power_fs, "; daya domain waktu =", power_time)
print("Soal 3: C0, C1, C2, C4 =", selected_C)
print("Soal 3: galat maksimum koefisien integral numerik =", np.max(np.abs(C_mid-pulse_coeff(k3))))
print("Soal 4: galat maksimum FT integral numerik =", np.max(np.abs(integral4-theory4)))
print("Soal 5: galat maksimum FT integral numerik =", np.max(np.abs(integral5-2/(3+1j*wcheck5))))
print("Soal 6: X(0), X(pi/2), X(pi) =", dtft([1, 2, 1], np.arange(3), [0, np.pi/2, np.pi]))
print("Soal 7: X(pi/3), X(7pi/3) =", test_X7[2:])
print("Soal 8: galat sifat transformasi vs DTFT langsung =", np.max(np.abs(Y8_direct-Y8_property)))
print("Soal 9: y[n] =", y9, "; galat kompleks Y-XH =", np.max(np.abs(Y9-X9*H9)))
print("Soal 10: H(pi/2) =", H0)
print("Soal 10: enam sampel pertama =", y10[:6])
print("Soal 10: galat rekursi vs solusi lengkap =", np.max(np.abs(y10-yss10-transient10)))
print("Semua pemeriksaan lulus. Sepuluh gambar PNG telah dibuat.")
