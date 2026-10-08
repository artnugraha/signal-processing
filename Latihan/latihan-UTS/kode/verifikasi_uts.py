"""Verifikasi solusi UTS dan pembuatan seluruh grafik konsep.

Jalankan dari direktori mana pun:
    python kode/verifikasi_uts.py

Opsional, untuk mengekstrak tiga cuplikan dari PDF sumber:
    python kode/verifikasi_uts.py --source-pdf "/lokasi/soal.pdf"

Pustaka wajib: numpy, matplotlib.
Pustaka opsional: pymupdf (hanya untuk --source-pdf).
"""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "gambar"
BLUE = "#176b9a"
ORANGE = "#c75a17"


def dft_langsung(x):
    """DFT tanpa normalisasi, menggunakan eksponen negatif."""
    x = np.asarray(x, dtype=complex)
    N = len(x)
    k = np.arange(N)[:, None]
    n = np.arange(N)[None, :]
    return np.exp(-2j * np.pi * k * n / N) @ x


def idft_langsung(X):
    """IDFT dengan normalisasi 1/N dan eksponen positif."""
    X = np.asarray(X, dtype=complex)
    N = len(X)
    n = np.arange(N)[:, None]
    k = np.arange(N)[None, :]
    return (np.exp(2j * np.pi * n * k / N) @ X) / N


def stem(ax, n, x, color=BLUE, label=None, offset=0):
    """Gambar sampel diskret; offset hanya membedakan seri yang bertumpuk."""
    marker, lines, baseline = ax.stem(np.asarray(n) + offset, x)
    plt.setp(marker, color=color, markersize=6)
    plt.setp(lines, color=color, linewidth=1.8)
    plt.setp(baseline, color="#777777", linewidth=0.7)
    if label:
        marker.set_label(label)
    ax.set_xlabel("Indeks sampel n")
    ax.set_ylabel("Amplitudo")
    ax.grid(alpha=0.2)
    ax.set_xticks(n)


def save(fig, filename):
    fig.savefig(FIGURES / filename, dpi=180, bbox_inches="tight")
    plt.close(fig)


def verifikasi():
    """Pemeriksaan matematis, termasuk efek konvolusi sirkular."""
    n = np.arange(16)
    x = np.cos(np.pi * n / 2)
    np.testing.assert_allclose(x[4:], x[:-4], atol=1e-12)
    assert not np.allclose(x[2:], x[:-2])

    energi = np.sum((0.5 ** np.arange(100)) ** 2)
    np.testing.assert_allclose(energi, 4 / 3)
    y = np.convolve([1, 2, 1], [1, 1])
    np.testing.assert_array_equal(y, [1, 3, 3, 1])

    # Impuls pada indeks 3 harus menggeser respons tiga sampel.
    impuls = [0, 0, 0, 1]
    np.testing.assert_array_equal(
        np.convolve(impuls, [1, 2, 1]), [0, 0, 0, 1, 2, 1]
    )
    kotak_n = np.arange(-2, 7)
    kotak = (kotak_n >= 0).astype(int) - (kotak_n >= 4).astype(int)
    np.testing.assert_array_equal(kotak, [0, 0, 1, 1, 1, 1, 0, 0, 0])

    batas = 0.1 * np.sin(200 * np.pi * np.arange(12) / 200)
    np.testing.assert_allclose(batas, 0, atol=1e-12)
    aman = 0.1 * np.sin(200 * np.pi * np.arange(3) / 300)
    np.testing.assert_allclose(aman, [0, 0.1 * np.sqrt(3) / 2,
                                    -0.1 * np.sqrt(3) / 2], atol=1e-12)

    h1 = np.array([1, 0, 1, 1])
    h2 = np.array([1, 1, 1])
    linear = np.convolve(h1, h2)
    np.testing.assert_array_equal(linear, [1, 1, 2, 2, 2, 1])
    frekuensi = np.fft.ifft(np.fft.fft(h1, 6) * np.fft.fft(h2, 6))
    np.testing.assert_allclose(frekuensi, linear, atol=1e-12)
    sirkular = np.fft.ifft(np.fft.fft(h1, 4) * np.fft.fft(h2, 4))
    np.testing.assert_allclose(sirkular, [3, 2, 2, 2], atol=1e-12)

    h = np.array([0, 1, 1, 0])
    H = dft_langsung(h)
    balik = idft_langsung(H)
    np.testing.assert_allclose(H, [2, -1 - 1j, 0, -1 + 1j], atol=1e-12)
    np.testing.assert_allclose(H, np.fft.fft(h), atol=1e-12)
    np.testing.assert_allclose(balik, h, atol=1e-12)
    np.testing.assert_allclose(np.sum(abs(h) ** 2),
                               np.sum(abs(H) ** 2) / 4, atol=1e-12)

    print("Semua pemeriksaan numerik berhasil.")
    print("Soal 2, energi =", energi)
    print("Soal 5, konvolusi =", y.tolist())
    print("Soal 11, periode bersama =", np.lcm(24, 36))
    print("Soal 13, sampel pada 200 Hz =", np.round(batas, 10))
    print("Esai 1, konvolusi linear =", linear.tolist())
    print("Esai 1, hasil DFT 6 titik =", np.round(frekuensi.real, 10))
    print("Esai 1, hasil DFT 4 titik (sirkular) =", np.round(sirkular.real, 10))
    print("Esai 2, DFT =", np.round(H, 10))
    print("Esai 2, IDFT =", np.round(balik.real, 10))


def buat_grafik():
    plt.rcParams.update({"font.size": 11, "axes.titlesize": 12})

    fig, ax = plt.subplots(2, 1, figsize=(9, 6), layout="constrained")
    n = np.arange(12)
    stem(ax[0], n, np.cos(np.pi * n / 2))
    ax[0].set_title(r"Soal 1: $x[n]=\cos(\pi n/2)$; periode dasar 4 sampel")
    ax[0].set_ylim(-1.3, 1.4)
    stem(ax[1], n, 0.5 ** n)
    ax[1].set_title(r"Soal 2: $x[n]=(0.5)^n u[n]$; amplitudo menurun")
    ax[1].set_ylim(-0.1, 1.2)
    save(fig, "01-periodik-energi.png")

    fig, ax = plt.subplots(2, 1, figsize=(9, 6), layout="constrained")
    n = np.arange(-1, 5)
    stem(ax[0], n, [0, 1, 2, 3, 0, 0], BLUE, "x[n]", -0.08)
    stem(ax[0], n, [0, 0, 1, 2, 3, 0], ORANGE, "x[n-1]", 0.08)
    ax[0].legend()
    ax[0].set_title("Soal 3: semua nilai tertunda satu sampel")
    n = np.arange(-2, 7)
    stem(ax[1], n, (n >= 0).astype(int) - (n >= 4).astype(int))
    ax[1].set_ylim(-0.15, 1.4)
    ax[1].set_title(r"Soal 9: $u[n]-u[n-4]$, aktif pada n = 0, 1, 2, 3")
    save(fig, "02-pergeseran-kotak.png")

    fig, ax = plt.subplots(2, 1, figsize=(9, 6), layout="constrained")
    stem(ax[0], np.arange(4), np.convolve([1, 2, 1], [1, 1]))
    ax[0].set_title("Soal 5: hasil konvolusi {1, 2, 1} dengan {1, 1}")
    stem(ax[1], np.arange(7), [0, 0, 0, 1, 2, 1, 0])
    ax[1].set_title(r"Soal 6: $h[n-3]$, aktif pada n = 3, 4, 5")
    save(fig, "03-konvolusi.png")

    fig, ax = plt.subplots(2, 1, figsize=(10, 6), layout="constrained")
    t = np.linspace(0, 0.03, 1501)
    for panel, fs in zip(ax, [200, 300]):
        ts = np.arange(int(round(0.03 * fs)) + 1) / fs
        samples = 0.1 * np.sin(200 * np.pi * ts)
        panel.plot(t * 1000, 0.1 * np.sin(200 * np.pi * t),
                   color=BLUE, label="Sinus analog 100 Hz")
        marker, lines, baseline = panel.stem(ts * 1000, samples)
        plt.setp(marker, color=ORANGE, markersize=7)
        plt.setp(lines, color=ORANGE, linewidth=1.7)
        plt.setp(baseline, color="#777777", linewidth=0.7)
        marker.set_label(f"Sampel pada {fs} Hz")
        panel.set(title=f"Soal 13: frekuensi sampling {fs} Hz",
                  xlabel="Waktu (ms)", ylabel="Amplitudo", ylim=(-0.13, 0.13))
        panel.grid(alpha=0.2)
        panel.legend(loc="upper right")
    save(fig, "04-batas-sampling.png")

    fig, ax = plt.subplots(3, 1, figsize=(9, 8), layout="constrained")
    for panel, values, title in zip(
        ax, [[1, 0, 1, 1], [1, 1, 1], [1, 1, 2, 2, 2, 1]],
        ["Sistem pertama: h1[n]", "Sistem kedua: h2[n]",
         "Respons total: konvolusi h1[n] dengan h2[n]"]
    ):
        stem(panel, np.arange(len(values)), values)
        panel.set_title(title)
        panel.set_ylim(-0.2, 2.5)
    save(fig, "05-esai-konvolusi.png")

    h = np.array([0, 1, 1, 0])
    H = dft_langsung(h)
    fig, ax = plt.subplots(3, 1, figsize=(9, 8), layout="constrained")
    stem(ax[0], np.arange(4), h)
    ax[0].set_title("Esai 2: deret awal h[n]")
    stem(ax[1], np.arange(4), np.abs(H))
    ax[1].set_title(r"Magnitudo DFT: $2,\sqrt{2},0,\sqrt{2}$")
    ax[1].set_xlabel("Indeks frekuensi k")
    ax[1].set_ylabel("Magnitudo")
    stem(ax[2], np.arange(4), idft_langsung(H).real)
    ax[2].set_title("Invers DFT mengembalikan deret awal")
    save(fig, "06-esai-dft.png")


def cuplikan_pdf(source_pdf):
    """Koordinat cuplikan khusus PDF soal yang menyertai latihan ini."""
    try:
        import fitz
    except ImportError as exc:
        raise SystemExit("Pasang pymupdf untuk menggunakan --source-pdf.") from exc

    # Nomor halaman berbasis nol; koordinat dalam point (1/72 inci).
    crops = [
        (2, (48, 369, 540, 729), "soal-07-asli.png"),
        (3, (48, 75, 540, 423), "soal-08-asli.png"),
        (5, (75, 99, 294, 139), "esai-01-diagram-asli.png"),
    ]
    with fitz.open(source_pdf) as doc:
        for page_index, rect, filename in crops:
            pix = doc[page_index].get_pixmap(
                matrix=fitz.Matrix(2, 2), clip=fitz.Rect(rect), alpha=False
            )
            pix.save(FIGURES / filename)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-pdf", type=Path, help="Lokasi PDF soal asli")
    args = parser.parse_args()
    FIGURES.mkdir(parents=True, exist_ok=True)
    verifikasi()
    buat_grafik()
    if args.source_pdf:
        cuplikan_pdf(args.source_pdf)
    print("Grafik disimpan pada:", FIGURES)


if __name__ == "__main__":
    main()
