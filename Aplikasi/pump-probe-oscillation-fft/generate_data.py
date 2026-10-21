"""Reproduksi CSV dan DAT sintetis. Jalankan dari folder mana pun.

Peringatan: skrip ini menimpa data/pump_probe_synthetic.csv dan .dat.
Parameter dibaca dari data/parameters.json. Grid indeks didesain untuk dt=5 fs.
"""
from pathlib import Path
import json
import numpy as np
from scipy.ndimage import gaussian_filter1d

ROOT = Path(__file__).resolve().parent
params = json.loads((ROOT / "data" / "parameters.json").read_text())

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

if __name__ == "__main__":
    t, y = synthesize(params)
    array = np.column_stack((t, y))
    np.savetxt(ROOT / "data" / "pump_probe_synthetic.csv", array,
               delimiter=",", header="delay_ps,deltaR_over_R", comments="", fmt="%.17g")
    np.savetxt(ROOT / "data" / "pump_probe_synthetic.dat", array,
               header="delay_ps deltaR_over_R", fmt="%.17g")
    print(f"Tersimpan {t.size} titik dalam format CSV dan DAT.")
