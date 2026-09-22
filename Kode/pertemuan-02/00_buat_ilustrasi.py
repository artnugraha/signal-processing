"""Bangun ulang seluruh SVG dan PNG dengan NumPy serta Matplotlib."""
from pathlib import Path
import runpy
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'Gambar' / 'pertemuan-02'
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'svg.fonttype': 'none', 'axes.spines.top': False,
    'axes.spines.right': False, 'savefig.facecolor': 'white',
    'axes.prop_cycle': plt.cycler(color=['#1765ad', '#e67e22', '#16875f', '#8054ac']),
})
BLUE, INK, PALE = '#1765ad', '#243746', '#edf5fb'


def simpan(fig, nama):
    for ekstensi in ['svg', 'png']:
        fig.savefig(OUT / f'{nama}.{ekstensi}', dpi=170, bbox_inches='tight')
    plt.close(fig)


def kanvas(lebar, tinggi, judul):
    fig, ax = plt.subplots(figsize=(lebar, tinggi))
    ax.set(xlim=(0, lebar), ylim=(0, tinggi))
    ax.set_aspect('equal')
    ax.axis('off')
    ax.text(lebar / 2, tinggi - 0.25, judul, ha='center', va='top',
            fontsize=15, fontweight='bold', color=INK)
    return fig, ax


def teks(ax, x, y, s, ukuran=11, **kwargs):
    ax.text(x, y, s, ha='center', va='center', color=INK,
            fontsize=ukuran, **kwargs)


def blok(ax, x, y, label, w=1.15, h=0.65):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
                 boxstyle='round,pad=0.02,rounding_size=0.05',
                 linewidth=1.5, edgecolor=BLUE, facecolor=PALE))
    teks(ax, x, y, label)


def panah(ax, a, b):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=13,
                                linewidth=1.4, color=INK, shrinkA=0, shrinkB=0))


def garis(ax, titik):
    ax.plot([p[0] for p in titik], [p[1] for p in titik], color=INK, lw=1.4)


def titik(ax, x, y):
    ax.plot(x, y, 'o', color=INK, markersize=4)


def jumlah(ax, x, y, simbol='+'):
    ax.add_patch(Circle((x, y), 0.24, facecolor=PALE, edgecolor=BLUE, lw=1.5))
    teks(ax, x, y, simbol, ukuran=17)


# Lima operator dasar, setiap panel memiliki masukan dan keluaran sendiri.
fig, ax = kanvas(11, 7.5, 'Komponen dasar sistem waktu-diskret')
for nomor, (judul, simbol, rumus) in enumerate([
    ('Penjumlah', '+', r'$w[n]=v_1[n]+v_2[n]$'),
    ('Pengali konstanta', 'K', r'$w[n]=Kv[n]$'),
    ('Pengali sinyal', '×', r'$w[n]=v_1[n]v_2[n]$'),
    ('Unit delay', 'D', r'$w[n]=v[n-1]$'),
    ('Unit advance', r'$D^{-1}$', r'$w[n]=v[n+1]$'),
]):
    kolom, baris = nomor % 2, nomor // 2
    cx, cy = 2.7 + 5.5 * kolom, 5.8 - 2.15 * baris
    teks(ax, cx, cy + 0.75, judul, ukuran=12, fontweight='bold')
    dua = nomor in [0, 2]
    if dua:
        jumlah(ax, cx, cy, simbol)
        panah(ax, (cx-1.5, cy), (cx-0.24, cy))
        panah(ax, (cx, cy+0.55), (cx, cy+0.24))
        teks(ax, cx-1.65, cy, r'$v_1$')
        teks(ax, cx+0.4, cy+0.5, r'$v_2$')
        awal = cx + 0.24
    else:
        blok(ax, cx, cy, simbol)
        panah(ax, (cx-1.5, cy), (cx-0.6, cy))
        teks(ax, cx-1.7, cy, r'$v$')
        awal = cx + 0.6
    panah(ax, (awal, cy), (cx+1.5, cy))
    teks(ax, cx+1.7, cy, r'$w$')
    teks(ax, cx, cy-0.62, rumus, ukuran=12)
teks(ax, 8.2, 1.45, 'Panah menunjukkan arah data.\nD menyimpan satu sampel.\nPemaju memerlukan sampel masa depan.', ukuran=11)
simpan(fig, 'komponen-dasar')

# Rata-rata tiga sampel: dua penunda berantai dan tiga cabang maju.
fig, ax = kanvas(10, 6.2, 'Realisasi nonrekursif: rata-rata tiga sampel')
panah(ax, (0.7, 4.8), (2, 4.8))
teks(ax, 0.65, 5.15, r'$x[n]$')
for yy, label in [(4.8, r'$x[n]$'), (2.9, r'$x[n-1]$'), (1.0, r'$x[n-2]$')]:
    titik(ax, 2, yy)
    panah(ax, (2, yy), (4.0, yy))
    blok(ax, 4.6, yy, '1/3')
    teks(ax, 3.1, yy+0.3, label)
for yy in [3.85, 1.95]:
    blok(ax, 2, yy, 'D', w=0.8)
    panah(ax, (2, yy+0.95), (2, yy+0.35))
    panah(ax, (2, yy-0.35), (2, yy-0.95))
jumlah(ax, 7.4, 2.9)
panah(ax, (5.2, 2.9), (7.16, 2.9))
garis(ax, [(5.2, 4.8), (7.4, 4.8)])
panah(ax, (7.4, 4.8), (7.4, 3.14))
garis(ax, [(5.2, 1.0), (7.4, 1.0)])
panah(ax, (7.4, 1.0), (7.4, 2.66))
panah(ax, (7.64, 2.9), (9.1, 2.9))
teks(ax, 9.1, 3.28, r'$y[n]$')
teks(ax, 5, 0.25, r'$y[n]=(x[n]+x[n-1]+x[n-2])/3$', ukuran=13)
simpan(fig, 'diagram-nonrekursif')

# Satu delay pada masukan dan satu delay pada jalur umpan balik.
fig, ax = kanvas(10, 6.2, 'Realisasi rekursif dengan umpan balik tertunda')
panah(ax, (0.6, 3), (2, 3))
teks(ax, 0.65, 3.4, r'$x[n]$')
titik(ax, 2, 3)
panah(ax, (2, 3), (3.2, 3))
blok(ax, 3.8, 3, '0.5')
jumlah(ax, 7.1, 3)
panah(ax, (4.4, 3), (6.86, 3))
garis(ax, [(2, 3), (2, 1.4)])
panah(ax, (2, 1.4), (2.6, 1.4))
blok(ax, 3.2, 1.4, 'D')
panah(ax, (3.8, 1.4), (4.4, 1.4))
teks(ax, 4.1, 0.95, r'$x[n-1]$')
blok(ax, 5, 1.4, '0.5')
garis(ax, [(5.6, 1.4), (7.1, 1.4)])
panah(ax, (7.1, 1.4), (7.1, 2.76))
panah(ax, (7.34, 3), (9.4, 3))
teks(ax, 9.35, 3.4, r'$y[n]$')
titik(ax, 8.3, 3)
garis(ax, [(8.3, 3), (8.3, 4.8)])
panah(ax, (8.3, 4.8), (7.0, 4.8))
blok(ax, 6.4, 4.8, 'D')
panah(ax, (5.8, 4.8), (5.1, 4.8))
teks(ax, 5.45, 5.2, r'$y[n-1]$')
blok(ax, 4.5, 4.8, '0.25')
garis(ax, [(3.9, 4.8), (3.2, 4.8), (3.2, 4), (7.1, 4)])
panah(ax, (7.1, 4), (7.1, 3.24))
teks(ax, 5, 0.35, r'$y[n]=0.25y[n-1]+0.5x[n]+0.5x[n-1]$', ukuran=13)
simpan(fig, 'diagram-rekursif')

# Rantai ADC: empat fungsi, label sinyal ditempatkan di bawah tahapnya.
fig, ax = kanvas(13, 3.7, 'Dari tegangan analog menuju kata biner')
pos = [1.8, 4.9, 8.0, 11.1]
nama = ['Pengondisian\n+ antialiasing', 'Sampling\n+ penahanan', 'Kuantisasi', 'Pengkodean']
catatan = ['Waktu kontinu\nAmplitudo kontinu', 'Nilai pada nTs\nBelum dibulatkan', 'L = 2^B tingkat\nAmplitudo berhingga', 'B bit per sampel\nContoh: 101']
for i, (xx, judul, label) in enumerate(zip(pos, nama, catatan)):
    blok(ax, xx, 2.1, judul, w=2.35, h=0.9)
    teks(ax, xx, 1.1, label, ukuran=11)
    if i < 3:
        panah(ax, (xx+1.2, 2.1), (pos[i+1]-1.2, 2.1))
teks(ax, 6.5, 0.25, 'Sampling mendiskretkan waktu; kuantisasi mendiskretkan amplitudo.', ukuran=12)
simpan(fig, 'alur-adc')

demo = [
    ('01_superposisi.py', 'superposisi'),
    ('02_invariansi_waktu.py', 'invariansi-waktu'),
    ('03_memori_kausalitas.py', 'memori-kausalitas'),
    ('04_persamaan_selisih.py', 'persamaan-selisih'),
    ('05_solusi_dan_kondisi_awal.py', 'kondisi-awal'),
    ('06_sampling_aliasing.py', 'sampling-aliasing'),
    ('07_sample_hold.py', 'sample-hold'),
    ('08_kuantisasi_pcm.py', 'kuantisasi-pcm'),
    ('09_sqnr.py', 'sqnr'),
    ('10_companding.py', 'companding'),
]
show_asli = plt.show
try:
    for skrip, nama in demo:
        def simpan_show(*args, nama=nama, **kwargs):
            for nomor in plt.get_fignums():
                simpan(plt.figure(nomor), nama)
        plt.show = simpan_show
        print('\nMenjalankan', skrip)
        runpy.run_path(str(Path(__file__).parent / skrip), run_name='__main__')
finally:
    plt.show = show_asli
print('\nSelesai: 14 SVG dan 14 PNG di', OUT)
