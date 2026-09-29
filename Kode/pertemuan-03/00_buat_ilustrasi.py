"""Membuat diagram sistem LTI dan menjalankan seluruh demo Kuliah 3.

Jalankan dari akar paket dengan:
python Kode/pertemuan-03/00_buat_ilustrasi.py
"""

from pathlib import Path
import runpy

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch


AKAR = Path(__file__).resolve().parents[2]
GAMBAR = AKAR / "Gambar" / "pertemuan-03"
GAMBAR.mkdir(parents=True, exist_ok=True)
BIRU, HIJAU, JINGGA, GELAP = "#225D91", "#087F72", "#B65020", "#253442"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "svg.fonttype": "none"})


def simpan(fig, nama):
    for ekstensi in ("svg", "png"):
        fig.savefig(GAMBAR / f"{nama}.{ekstensi}", dpi=180,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)


def kanvas(lebar, tinggi):
    fig, ax = plt.subplots(figsize=(lebar, tinggi))
    ax.set_xlim(0, lebar)
    ax.set_ylim(0, tinggi)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def kotak(ax, x, y, w, h, label, warna=BIRU):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
                 boxstyle="round,pad=0.03,rounding_size=0.08",
                 ec=warna, fc="#F3F7FB", lw=1.7))
    ax.text(x, y, label, ha="center", va="center", fontsize=14, color=warna)


def panah(ax, x1, y1, x2, y2, warna=GELAP):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                 mutation_scale=14, lw=1.5, color=warna))


def jumlah(ax, x, y):
    ax.add_patch(Circle((x, y), 0.23, ec=HIJAU, fc="#EFFAF7", lw=1.7))
    ax.text(x, y, "+", ha="center", va="center", fontsize=18, color=HIJAU)


def gambar_sistem_lti():
    fig, ax = kanvas(9, 2.5)
    ax.text(0.55, 1.25, r"$x[n]$", ha="center", va="center", fontsize=15)
    panah(ax, 1.05, 1.25, 2.55, 1.25)
    kotak(ax, 3.7, 1.25, 2.3, 1.0, r"Sistem LTI $h[n]$")
    panah(ax, 4.85, 1.25, 6.35, 1.25)
    ax.text(7.55, 1.25, r"$y[n]=x[n]*h[n]$", ha="center", va="center", fontsize=15)
    simpan(fig, "sistem-lti-konvolusi")


def gambar_korelasi_pergeseran():
    fig, axes = plt.subplots(2, 1, figsize=(9, 5.2), sharex=False)
    for awal in (0, 4, 8):
        axes[0].add_patch(plt.Rectangle((awal, 0), 2, 1, ec=BIRU, fc="#DDEAF5", lw=1.7))
        axes[0].add_patch(plt.Rectangle((awal+1.5, -1.35), 2, 1, ec=JINGGA,
                                        fc="#FBE7D8", lw=1.7))
    axes[0].text(10.4, 0.5, r"$x_1[n]$", color=BIRU, fontsize=13)
    axes[0].text(10.4, -0.85, r"$x_2[n]$", color=JINGGA, fontsize=13)
    axes[0].axhline(0, color=GELAP, lw=1)
    axes[0].set_ylim(-1.7, 1.35); axes[0].set_xlim(-0.5, 12.2); axes[0].axis("off")
    axes[0].set_title("Pola identik dapat memiliki pergeseran")

    axes[1].plot([1.5, 4.2], [0.1, 2.4], color=JINGGA, lw=2)
    axes[1].plot([5.2, 7.9], [0.1, 2.4], color=BIRU, lw=2)
    axes[1].annotate("", xy=(5.25, -0.05), xytext=(1.45, -0.05),
                     arrowprops={"arrowstyle": "<->", "color": GELAP, "lw": 1.5})
    axes[1].text(3.35, -0.32, r"$j$", ha="center", fontsize=14)
    axes[1].text(3.1, 2.1, r"$x_2: n+j$", color=JINGGA, fontsize=13)
    axes[1].text(6.7, 2.1, r"$x_1: n$", color=BIRU, fontsize=13)
    axes[1].axhline(0, color=GELAP, lw=1)
    axes[1].set_xlim(0, 9); axes[1].set_ylim(-0.45, 2.8); axes[1].axis("off")
    axes[1].set_title("Makna geometris lag: $x_2[n]$ digeser ke kiri")
    fig.tight_layout(h_pad=1.2)
    simpan(fig, "korelasi-pergeseran")


def gambar_efek_akhir():
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    n = 9
    j = list(range(n + 1))
    terukur = [1-k/n for k in j]
    ax.plot(j, terukur, "o-", color=BIRU, label=r"$r_{12}(j)$ tanpa koreksi")
    ax.axhline(1, color=HIJAU, ls="--", label=r"$r_{12}(j)_{\mathrm{true}}$")
    ax.fill_between(j, terukur, 1, color="#FBE7D8", alpha=.8,
                    label="bagian akibat efek akhir")
    ax.set(xlabel="Lag, $j$", ylabel="Korelasi relatif", xlim=(0, n), ylim=(0, 1.12))
    ax.grid(alpha=.25); ax.legend(frameon=False, loc="lower left")
    fig.tight_layout(); simpan(fig, "efek-akhir-korelasi")


def gambar_interkoneksi():
    fig, axes = plt.subplots(3, 1, figsize=(10, 8.2))
    for ax in axes:
        ax.set_xlim(0, 10); ax.set_ylim(0, 3); ax.axis("off"); ax.set_aspect("equal")

    ax = axes[0]
    panah(ax, .4, 1.5, 1.4, 1.5); kotak(ax, 2.2, 1.5, 1.6, .8, r"$h_1[n]$")
    panah(ax, 3, 1.5, 4.2, 1.5); kotak(ax, 5, 1.5, 1.6, .8, r"$h_2[n]$")
    panah(ax, 5.8, 1.5, 7.0, 1.5)
    ax.text(8.4, 1.5, r"$h=h_1*h_2$", va="center", fontsize=14)
    ax.text(.2, 2.55, "(a) Hubungan seri", color=BIRU, fontsize=13, weight="bold")

    ax = axes[1]
    ax.plot([.7, 1.5, 1.5], [1.5, 1.5, 2.15], color=GELAP, lw=1.5)
    ax.plot([1.5, 1.5], [1.5, .85], color=GELAP, lw=1.5)
    kotak(ax, 3, 2.15, 1.7, .7, r"$h_1[n]$"); kotak(ax, 3, .85, 1.7, .7, r"$h_2[n]$")
    panah(ax, 3.85, 2.15, 5.1, 2.15); panah(ax, 3.85, .85, 5.1, .85)
    ax.plot([5.1, 5.1], [2.15, 1.73], color=GELAP, lw=1.5)
    ax.plot([5.1, 5.1], [.85, 1.27], color=GELAP, lw=1.5); jumlah(ax, 5.1, 1.5)
    panah(ax, 5.33, 1.5, 6.7, 1.5)
    ax.text(8.0, 1.5, r"$h=h_1+h_2$", va="center", fontsize=14)
    ax.text(.2, 2.55, "(b) Hubungan paralel", color=BIRU, fontsize=13, weight="bold")

    ax = axes[2]
    ax.plot([.5, 1.2, 1.2], [2.25, 2.25, .7], color=GELAP, lw=1.5)
    kotak(ax, 2.6, 2.25, 1.5, .65, r"$h_1[n]$")
    kotak(ax, 2.0, 1.05, 1.5, .65, r"$h_2[n]$")
    ax.plot([2.75, 3.25, 3.25], [1.05, 1.05, .55], color=GELAP, lw=1.5)
    kotak(ax, 4.2, 1.05, 1.5, .65, r"$h_3[n]$")
    kotak(ax, 4.2, .25, 1.5, .5, r"$h_4[n]$")
    panah(ax, 4.95, 1.05, 6.0, 1.05); panah(ax, 4.95, .25, 6.0, .25)
    ax.plot([6, 6], [.25, .82], color=GELAP, lw=1.5); jumlah(ax, 6, 1.05)
    ax.plot([6, 6.9, 6.9], [1.28, 1.28, 2.02], color=GELAP, lw=1.5)
    panah(ax, 3.35, 2.25, 6.9, 2.25); jumlah(ax, 6.9, 2.25)
    panah(ax, 7.13, 2.25, 8.5, 2.25)
    ax.text(.2, 2.65, "(c) Kombinasi seri–paralel", color=BIRU, fontsize=13, weight="bold")
    fig.tight_layout(h_pad=.6); simpan(fig, "interkoneksi-lti")


gambar_sistem_lti()
gambar_korelasi_pergeseran()
gambar_efek_akhir()
gambar_interkoneksi()

for berkas in [
    "01_konvolusi_diskret.py",
    "02_konvolusi_grafis.py",
    "03_konvolusi_siklik.py",
    "04_korelasi.py",
    "05_autokorelasi_dan_radar.py",
    "06_konvolusi_kontinu.py",
]:
    print(f"Menjalankan {berkas}")
    runpy.run_path(str(Path(__file__).parent / berkas), run_name="__main__")

print(f"Seluruh ilustrasi disimpan di {GAMBAR}")
