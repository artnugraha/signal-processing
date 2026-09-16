"""Membuat seluruh ilustrasi SVG/PNG dari diagram dan demo kuliah.

Jalankan: python Kode/pertemuan-02/00_buat_ilustrasi.py
Pustaka tambahan di luar NumPy dan Matplotlib tidak diperlukan.
"""

from pathlib import Path
import runpy

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch


AKAR = Path(__file__).resolve().parents[2]
GAMBAR = AKAR / "Gambar" / "pertemuan-02"
GAMBAR.mkdir(parents=True, exist_ok=True)
BIRU = "#225D91"
HIJAU = "#087F72"
JINGGA = "#B65020"
GELAP = "#253442"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.labelsize": 12,
    "legend.fontsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "svg.fonttype": "none",
    "axes.prop_cycle": plt.cycler(color=[BIRU, JINGGA, HIJAU, "#8456A0"]),
})


def simpan(fig, nama):
    for ekstensi in ["svg", "png"]:
        fig.savefig(GAMBAR / f"{nama}.{ekstensi}", dpi=170,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)


def kanvas(lebar, tinggi):
    fig, ax = plt.subplots(figsize=(lebar, tinggi))
    ax.set_xlim(0, lebar)
    ax.set_ylim(0, tinggi)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def teks(ax, x, y, isi, ukuran=14, warna=GELAP, ha="center"):
    ax.text(x, y, isi, ha=ha, va="center", fontsize=ukuran, color=warna)


def kotak(ax, x, y, w, h, isi, warna=BIRU):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                 boxstyle="round,pad=0.02,rounding_size=0.08",
                 linewidth=1.7, edgecolor=warna, facecolor="#F3F7FB"))
    teks(ax, x, y, isi, 16, warna)


def panah(ax, x1, y1, x2, y2, warna=GELAP):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                 arrowstyle="-|>", mutation_scale=14, linewidth=1.6,
                 color=warna, shrinkA=0, shrinkB=0))


def garis(ax, titik, warna=GELAP):
    p = np.array(titik)
    ax.plot(p[:, 0], p[:, 1], color=warna, linewidth=1.6)


def simpul(ax, x, y):
    ax.add_patch(Circle((x, y), 0.045, color=GELAP))


def penjumlah(ax, x, y, r=0.24):
    ax.add_patch(Circle((x, y), r, linewidth=1.8,
                        edgecolor=HIJAU, facecolor="#F0FAF7"))
    teks(ax, x, y, "+", 20, HIJAU)


def gambar_blok_dasar():
    fig, ax = kanvas(10, 4.6)
    teks(ax, 0.3, 3.75, "Penjumlah", 14, ha="left")
    teks(ax, 0.3, 2.25, "Pengali", 14, ha="left")
    teks(ax, 0.3, 0.8, "Penunda", 14, ha="left")

    teks(ax, 3.1, 4.1, r"$v_1[n]$", 14)
    teks(ax, 3.1, 3.4, r"$v_2[n]$", 14)
    garis(ax, [(3.6, 4.1), (4.35, 4.1)])
    panah(ax, 4.35, 4.1, 4.8, 3.85)
    garis(ax, [(3.6, 3.4), (4.35, 3.4)])
    panah(ax, 4.35, 3.4, 4.8, 3.65)
    penjumlah(ax, 5, 3.75)
    panah(ax, 5.25, 3.75, 6.5, 3.75)
    teks(ax, 6.75, 3.75, r"$w[n]=v_1[n]+v_2[n]$", 14, ha="left")

    for y, simbol, hasil in [(2.25, r"$c$", r"$w[n]=cv[n]$"),
                              (0.8, r"$D$", r"$w[n]=v[n-1]$")]:
        teks(ax, 3.1, y, r"$v[n]$", 14)
        panah(ax, 3.65, y, 4.4, y)
        kotak(ax, 5, y, 1.2, 0.7, simbol)
        panah(ax, 5.6, y, 6.5, y)
        teks(ax, 6.75, y, hasil, 14, ha="left")
    simpan(fig, "blok-dasar")


def gambar_nonrekursif():
    fig, ax = kanvas(10, 5.2)
    teks(ax, 0.2, 4.0, r"$x[n]$", 15, ha="left")
    panah(ax, 0.85, 4, 1.5, 4)
    panah(ax, 1.5, 4, 2.55, 4)
    kotak(ax, 3.1, 4, 1.1, 0.7, r"$D$")
    panah(ax, 3.65, 4, 4.6, 4)
    panah(ax, 4.6, 4, 5.65, 4)
    kotak(ax, 6.2, 4, 1.1, 0.7, r"$D$")
    panah(ax, 6.75, 4, 7.7, 4)

    for x, nama in [(1.5, r"$x[n]$"), (4.6, r"$x[n-1]$"), (7.7, r"$x[n-2]$")]:
        simpul(ax, x, 4)
        teks(ax, x, 4.65, nama, 15)
        panah(ax, x, 4, x, 2.85)
        kotak(ax, x, 2.45, 1.0, 0.8, r"$1/3$")

    garis(ax, [(1.5, 2.05), (1.5, 1.1)])
    panah(ax, 1.5, 1.1, 4.35, 1.1)
    panah(ax, 4.6, 2.05, 4.6, 1.35)
    garis(ax, [(7.7, 2.05), (7.7, 1.1)])
    panah(ax, 7.7, 1.1, 4.85, 1.1)
    penjumlah(ax, 4.6, 1.1)
    garis(ax, [(4.6, 0.85), (4.6, 0.35)])
    panah(ax, 4.6, 0.35, 8.6, 0.35)
    teks(ax, 8.8, 0.35, r"$y[n]$", 15, ha="left")
    simpan(fig, "diagram-nonrekursif")


def gambar_rekursif():
    fig, ax = kanvas(10, 4.3)
    teks(ax, 0.2, 3.2, r"$x[n]$", 15, ha="left")
    panah(ax, 0.95, 3.2, 1.85, 3.2)
    kotak(ax, 2.4, 3.2, 1.1, 0.8, r"$b$")
    panah(ax, 2.95, 3.2, 4.45, 3.2)
    penjumlah(ax, 4.7, 3.2)
    panah(ax, 4.95, 3.2, 8.5, 3.2)
    simpul(ax, 7.6, 3.2)
    teks(ax, 8.8, 3.2, r"$y[n]$", 15)

    garis(ax, [(7.6, 3.2), (7.6, 1.2)])
    panah(ax, 7.6, 1.2, 7.0, 1.2)
    kotak(ax, 6.45, 1.2, 1.1, 0.8, r"$D$")
    panah(ax, 5.9, 1.2, 5.25, 1.2)
    kotak(ax, 4.7, 1.2, 1.1, 0.8, r"$a$")
    garis(ax, [(4.15, 1.2), (3.5, 1.2), (3.5, 2.1), (4.7, 2.1)])
    panah(ax, 4.7, 2.1, 4.7, 2.95)
    teks(ax, 5.52, 0.62, r"$y[n-1]$", 14)
    teks(ax, 6.45, 0.14, r"Isi awal $D$: $y[-1]$", 12)
    teks(ax, 5.5, 3.95, r"$y[n]=a\,y[n-1]+b\,x[n]$", 17)
    simpan(fig, "diagram-rekursif")


def gambar_memori():
    fig, axes = plt.subplots(3, 1, figsize=(9, 6.6), sharex=True)
    rel = np.arange(-3, 4)
    data = np.array([0.4, 0.8, 1.1, 0.6, 0.9, 0.4, 0.7])
    kasus = [([0], "Tanpa memori: hanya sampel sekarang", BIRU),
             ([-2, -1, 0], "Rata-rata kausal: sekarang dan masa lalu", HIJAU),
             ([-1, 0, 1], "Rata-rata simetris: memerlukan masa depan", JINGGA)]
    for ax, (dipakai, nama, warna) in zip(axes, kasus):
        ax.axvspan(-3.6, -0.12, color="#EFF5FA")
        ax.axvspan(0.12, 3.6, color="#FCF2E9")
        ax.axvline(0, color=GELAP, linestyle=":", linewidth=1.2)
        ax.vlines(rel, 0, data, color="#C7CDD3", linewidth=2)
        ax.scatter(rel, data, color="#C7CDD3", s=40, zorder=3)
        pilih = np.isin(rel, dipakai)
        ax.vlines(rel[pilih], 0, data[pilih], color=warna, linewidth=3)
        ax.scatter(rel[pilih], data[pilih], color=warna, s=65, zorder=4)
        ax.set_ylim(0, 1.65)
        ax.set_xlim(-3.6, 3.6)
        ax.set_yticks([])
        ax.text(0.02, 0.92, nama, va="top", transform=ax.transAxes,
                color=warna, fontsize=12)
        ax.set_ylabel("x[k]")
        ax.spines["left"].set_visible(False)
    axes[-1].set_xticks(rel, [r"$n_*-3$", r"$n_*-2$", r"$n_*-1$", r"$n_*$",
                              r"$n_*+1$", r"$n_*+2$", r"$n_*+3$"])
    axes[-1].set_xlabel("Indeks sampel k; keluaran dihitung pada n*")
    fig.tight_layout(h_pad=1.3)
    simpan(fig, "memori-kausalitas")


gambar_blok_dasar()
gambar_nonrekursif()
gambar_rekursif()
gambar_memori()

demo = [
    ("01_superposisi.py", "superposisi"),
    ("02_invariansi_waktu.py", "invariansi-waktu"),
    ("03_nonrekursif.py", "rata-rata-tiga-sampel"),
    ("04_respons_dan_kondisi_awal.py", "dekomposisi-respons"),
    ("05_stabilitas_orde_satu.py", "stabilitas-orde-satu"),
    ("06_persamaan_selisih_umum.py", None),
    ("07_sensor_temperatur.py", "sensor-temperatur"),
]

show_asli = plt.show
for berkas, nama in demo:
    def simpan_demo(*args, **kwargs):
        for nomor in plt.get_fignums():
            simpan(plt.figure(nomor), nama)

    plt.show = simpan_demo
    print(f"\nMenjalankan {berkas}")
    runpy.run_path(str(Path(__file__).parent / berkas), run_name="__main__")
plt.show = show_asli
print(f"\nIlustrasi disimpan di {GAMBAR}")
