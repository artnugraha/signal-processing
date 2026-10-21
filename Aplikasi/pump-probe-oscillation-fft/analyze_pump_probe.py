"""Versi skrip dari seluruh sel analisis. Membaca CSV, menyimpan hasil dan PNG."""
import matplotlib
matplotlib.use("Agg")
from pathlib import Path
import json
import numpy as np
import scipy
from scipy.optimize import curve_fit
from scipy.signal import find_peaks, windows
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt
from IPython.display import display, Markdown

plt.rcParams.update({
    "figure.figsize": (11, 4.5), "figure.dpi": 120,
    "font.size": 11, "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True,
    "grid.alpha": 0.18, "axes.titleweight": "bold",
})
BLUE, ORANGE, GREEN = "#1565a8", "#d96824", "#15827c"
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "pump_probe_synthetic.csv"
if not DATA.is_file():
    raise FileNotFoundError(
        "CSV tidak ditemukan. Ekstrak seluruh ZIP dan buka notebook dari folder "
        "yang memuat notebook ini dan subfolder data."
    )
print(f"NumPy {np.__version__} | SciPy {scipy.__version__}")

raw = np.genfromtxt(DATA, delimiter=",", names=True)
t = np.asarray(raw["delay_ps"])
y = np.asarray(raw["deltaR_over_R"])
assert np.all(np.isfinite(t)) and np.all(np.isfinite(y))
assert np.all(np.diff(t) > 0), "Time delay harus meningkat."
dt_ps = float(np.mean(np.diff(t)))
assert np.allclose(np.diff(t), dt_ps, rtol=1e-8, atol=1e-12), (
    "FFT biasa memerlukan sampling seragam."
)
assert dt_ps > 0
print(f"Jumlah sampel       : {t.size}")
print(f"Rentang delay       : {t[0]:.3f} sampai {t[-1]:.3f} ps")
print(f"Langkah delay       : {dt_ps:.6f} ps = {dt_ps * 1000:.1f} fs")
print(f"Frekuensi Nyquist   : {1 / (2 * dt_ps):.1f} THz")
print("\nLima baris pertama [delay_ps, deltaR_over_R]:")
print(np.column_stack((t, y))[:5])

fig_time, ax = plt.subplots(2, 1, figsize=(11, 7), constrained_layout=True)
ax[0].plot(t, 1e3 * y, color=BLUE, lw=1.0)
ax[0].axvline(0, color="0.35", ls="--", lw=1, label="Pump tiba")
ax[0].set(xlim=(-1, 12), ylabel=r"$\Delta R/R_0$ ($\times 10^{-3}$)",
          title="Data sintetis asli: respons pump–probe dengan dua mode getaran")
ax[0].legend(loc="upper right")
ax[1].plot(t, 1e3 * y, color=BLUE, lw=1.3)
ax[1].set(xlim=(0, 3), xlabel="Time delay pump–probe (ps)",
          ylabel=r"$\Delta R/R_0$ ($\times 10^{-3}$)",
          title="Pembesaran 0–3 ps: superposisi osilasi di atas latar belakang")
plt.show()

analysis_mask = (t >= 0.25 - 1e-10) & (t <= 12.0 + 1e-10)
ta, ya = t[analysis_mask], y[analysis_mask]

def background_milli(t_ps, B_milli, tau_ps, C_milli):
    return B_milli * np.exp(-t_ps / tau_ps) + C_milli

popt, pcov = curve_fit(
    background_milli, ta, 1e3 * ya,
    p0=(0.8, 4.0, 0.02),
    bounds=([0.0, 0.1, -1.0], [10.0, 30.0, 1.0]),
    maxfev=20000,
)
background = 1e-3 * background_milli(ta, *popt)
residual = ya - background
x = residual - residual.mean()
M = x.size
w = windows.hann(M, sym=False)
xw = w * x
print(f"B_fit       = {popt[0] * 1e-3:.6g}")
print(f"tau_bg_fit  = {popt[1]:.4f} ps")
print(f"C_fit       = {popt[2] * 1e-3:.6g}")
print(f"Sampel FFT  = {M}, dari {ta[0]:.2f} sampai {ta[-1]:.2f} ps")

fig_pre, ax = plt.subplots(2, 1, figsize=(11, 7), sharex=True,
                           constrained_layout=True)
ax[0].plot(ta, 1e3 * ya, color=BLUE, lw=0.9, label="Data asli")
ax[0].plot(ta, 1e3 * background, color=ORANGE, lw=2, label="Fit latar belakang")
ax[0].set(ylabel=r"$\Delta R/R_0$ ($\times 10^{-3}$)",
          title="Latar belakang diestimasi dari data")
ax[0].legend()
ax[1].plot(ta, 1e3 * x, color="0.65", lw=0.9, label="Residual tanpa rerata")
ax[1].plot(ta, 1e3 * xw, color=GREEN, lw=1.2, label="Residual × Hann")
ax[1].set(xlim=(0.25, 12), xlabel="Time delay pump–probe (ps)",
          ylabel=r"Residual ($\times 10^{-3}$)",
          title="Sinyal yang masuk ke FFT")
ax[1].legend()
plt.show()

N_fft = 4 * (1 << (M - 1).bit_length())
freq_THz = np.fft.rfftfreq(N_fft, d=dt_ps)
F = dt_ps * np.fft.rfft(xw, n=N_fft)
intensity = np.abs(F) ** 2
band = (freq_THz >= 0.5) & (freq_THz <= 8.0)
I_rel = intensity / intensity[band].max()

band_indices = np.flatnonzero(band)
df_grid = freq_THz[1] - freq_THz[0]
minimum_separation_bins = max(1, int(np.ceil(0.4 / df_grid)))
local_peaks, properties = find_peaks(
    I_rel[band], prominence=0.03, distance=minimum_separation_bins
)
candidate_indices = band_indices[local_peaks]
if candidate_indices.size < 2:
    raise RuntimeError("Kurang dari dua puncak terdeteksi; periksa data atau ambang.")
strongest = candidate_indices[np.argsort(I_rel[candidate_indices])[-2:]]
peak_indices = strongest[np.argsort(freq_THz[strongest])]
peak_frequencies = freq_THz[peak_indices]

print(f"N_fft                         : {N_fft}")
print(f"Jarak bin tanpa zero-padding  : {1 / (M * dt_ps):.6f} THz")
print(f"Jarak grid dengan padding     : {df_grid:.6f} THz")
print(f"Puncak yang lolos kriteria     : {candidate_indices.size}")
print("\nMode | Frekuensi FFT (THz) | Periode (ps) | Intensitas relatif")
for i, k in enumerate(peak_indices, start=1):
    print(f"{i:4d} | {freq_THz[k]:19.6f} | {1/freq_THz[k]:12.6f} | {I_rel[k]:.6f}")

fig_fft, ax = plt.subplots(2, 1, figsize=(11, 7), sharex=True,
                           gridspec_kw={"height_ratios": [2, 1]},
                           constrained_layout=True)
ax[0].plot(freq_THz, I_rel, color=BLUE, lw=1.8)
ax[0].fill_between(freq_THz, I_rel, color=BLUE, alpha=0.10)
for i, k in enumerate(peak_indices):
    color = [ORANGE, GREEN][i]
    ax[0].plot(freq_THz[k], I_rel[k], "o", color=color, ms=7)
    ax[0].annotate(f"Mode {i+1}: {freq_THz[k]:.3f} THz",
                   (freq_THz[k], I_rel[k]), xytext=(16, -5 if i == 0 else 30),
                   textcoords="offset points", color=color,
                   arrowprops={"arrowstyle": "-", "color": color})
ax[0].set(ylabel=r"Intensitas Fourier relatif $|F|^2 / |F|^2_{\max}$",
          ylim=(-0.02, 1.15), title="FFT menemukan dua mode getaran utama")
ax[1].semilogy(freq_THz, np.maximum(I_rel, 1e-12), color=BLUE, lw=1)
ax[1].set(xlim=(0.5, 8), ylim=(1e-7, 2), xlabel="Frekuensi (THz)",
          ylabel="Intensitas relatif (log)", title="Puncak dan latar derau")
plt.show()

bins_to_check = np.unique(np.r_[0, 1, peak_indices,
                                peak_indices - 1, peak_indices + 1])
n = np.arange(M)
dft_direct = dt_ps * np.array([
    np.sum(xw * np.exp(-2j * np.pi * k * n / N_fft))
    for k in bins_to_check
])
fft_selected = F[bins_to_check]
relative_error = np.max(np.abs(dft_direct - fft_selected)) / np.max(np.abs(F))
print(f"Jumlah bin yang diperiksa: {bins_to_check.size}")
print(f"Galat maksimum / amplitudo spektrum maksimum: {relative_error:.3e}")
np.testing.assert_allclose(dft_direct, fft_selected, rtol=1e-10, atol=1e-15)
print("Lulus: penjumlahan DFT dan FFT menghasilkan nilai yang sama.")

params = json.loads((ROOT / "data" / "parameters.json").read_text())
true_frequencies = np.sort([m["frequency_THz"] for m in params["modes"]])
frequency_errors = peak_frequencies - true_frequencies
table = ["| Mode | Pembangkit (THz) | Puncak FFT (THz) | Selisih (THz) |",
         "| --- | ---: | ---: | ---: |"]
for i, (truth, measured, error) in enumerate(
        zip(true_frequencies, peak_frequencies, frequency_errors), start=1):
    table.append(f"| {i} | {truth:.3f} | {measured:.6f} | {error:+.6f} |")
display(Markdown("\n".join(table)))
assert np.all(np.abs(frequency_errors) < 0.05)
print("Kedua frekuensi berhasil ditemukan dengan selisih kurang dari 0,05 THz.")

f_native = np.fft.rfftfreq(M, d=dt_ps)
I_native = np.abs(dt_ps * np.fft.rfft(xw)) ** 2 / intensity[band].max()
I_rect = np.abs(dt_ps * np.fft.rfft(x, n=N_fft)) ** 2 / intensity[band].max()
fig_compare, axes = plt.subplots(1, 2, figsize=(12, 4), constrained_layout=True)
for ax, center in zip(axes, peak_frequencies):
    ax.plot(freq_THz, I_rect, color="0.6", lw=1, label="Tanpa Hann; padding")
    ax.plot(freq_THz, I_rel, color=BLUE, lw=1.6, label="Hann; padding")
    near = np.abs(f_native - center) < 0.5
    ax.plot(f_native[near], I_native[near], "o", color=ORANGE,
            ms=4, label="Hann; tanpa padding")
    ax.set(xlim=(center - 0.5, center + 0.5), xlabel="Frekuensi (THz)",
           ylabel="Kuadrat magnitudo, pembagi sama",
           title=f"Sekitar {center:.2f} THz")
axes[0].legend(fontsize=9)
plt.show()

def synthesize(p):
    dt = p["dt_ps"]
    # Margin di kiri/kanan mencegah efek batas filter dalam data tersimpan.
    grid_index = np.arange(-400, 2801)
    t_ext = grid_index * dt
    positive = t_ext >= 0
    response = np.zeros_like(t_ext)
    tp = t_ext[positive]
    response[positive] = p["background_amplitude"] * np.exp(
        -tp / p["background_tau_ps"]
    )
    for mode in p["modes"]:
        response[positive] += (
            mode["amplitude"] * np.exp(-tp / mode["tau_ps"])
            * np.cos(2 * np.pi * mode["frequency_THz"] * tp + mode["phase_rad"])
        )
    sigma_ps = p["irf_fwhm_ps"] / (2 * np.sqrt(2 * np.log(2)))
    blurred = gaussian_filter1d(response, sigma=sigma_ps / dt,
                                mode="constant", cval=0.0, truncate=6.0)
    take = (grid_index >= -200) & (grid_index <= 2400)
    delay_ps = t_ext[take]
    noiseless = p["offset"] + blurred[take]
    rng = np.random.default_rng(p["seed"])
    measured = noiseless + rng.normal(0, p["noise_std"], delay_ps.size)
    return delay_ps, measured

t_regenerated, y_regenerated = synthesize(params)
np.testing.assert_allclose(t_regenerated, t, rtol=0, atol=1e-14)
np.testing.assert_allclose(y_regenerated, y, rtol=1e-11, atol=1e-15)
print("Lulus: kode pembangkit mereproduksi seluruh data CSV.")

SAVE_RESULTS = True
if SAVE_RESULTS:
    results_dir = ROOT / "results"
    results_dir.mkdir(exist_ok=True)
    np.savetxt(results_dir / "fourier_spectrum.csv",
               np.column_stack((freq_THz, intensity, I_rel)),
               delimiter=",", comments="", fmt="%.17g",
               header="frequency_THz,abs_F_squared_ps2,relative_intensity")
    np.savetxt(results_dir / "detected_peaks.csv",
               np.column_stack((peak_frequencies, 1 / peak_frequencies,
                                I_rel[peak_indices])),
               delimiter=",", comments="", fmt="%.17g",
               header="frequency_THz,period_ps,relative_intensity")
    print("Hasil numerik telah diperbarui di folder results.")
else:
    print("Hasil bawaan tersedia dalam folder results; tidak ada berkas ditimpa.")

import io
fig_dir = ROOT / "figures"
fig_dir.mkdir(exist_ok=True)
for fig, name in [(fig_time, "01_time_trace.png"),
                  (fig_pre, "02_preprocessing.png"),
                  (fig_fft, "03_fourier_intensity.png"),
                  (fig_compare, "04_window_padding.png")]:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=170, bbox_inches="tight")
    (fig_dir / name).write_bytes(buf.getvalue())
print("Empat gambar PNG tersimpan di folder figures.")

